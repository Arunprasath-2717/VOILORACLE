"""
Kronaxis — Real-Time Geo-Intelligence News Fetcher
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fetches live news from multiple APIs (GNews, NewsData.io, GDELT, NewsAPI, Currents)
and classifies them into geointelligence categories grouped by region.
"""

import logging
import time
import hashlib
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests  # type: ignore
import feedparser  # type: ignore

import backend.config as config
from backend import database

logger = logging.getLogger("Kronaxis.geo_news")

# ── Intelligence Categories ──────────────────────────────────────────────────
INTEL_CATEGORIES = {
    "Geopolitical": {
        "icon": "🌍",
        "color": "#ef4444",
        "keywords": [
            "geopolitical", "sanctions", "diplomacy", "embassy", "territorial",
            "sovereignty", "annexation", "border dispute", "ceasefire", "peace talks",
            "coup", "regime", "protest", "uprising", "revolution", "referendum",
            "nato", "un security council", "g7", "g20", "brics", "asean",
            "foreign policy", "bilateral", "multilateral", "alliance", "treaty",
            "imperialism", "colonialism", "separatist", "independence movement",
        ],
    },
    "Cybersecurity": {
        "icon": "🛡️",
        "color": "#8b5cf6",
        "keywords": [
            "cyber attack", "cybersecurity", "hack", "ransomware", "malware",
            "data breach", "phishing", "zero-day", "vulnerability", "exploit",
            "ddos", "cyber warfare", "encryption", "firewall", "spyware",
            "dark web", "cyber espionage", "digital forensics", "apt", "threat actor",
            "critical infrastructure attack", "scada", "ics security",
        ],
    },
    "Military & Defense": {
        "icon": "⚔️",
        "color": "#f97316",
        "keywords": [
            "military", "defense", "army", "navy", "air force", "missile",
            "nuclear", "weapons", "drone strike", "war", "conflict", "invasion",
            "troops", "deployment", "artillery", "fighter jet", "submarine",
            "ammunition", "arms deal", "military exercise", "special forces",
            "pentagon", "defense budget", "military base", "airstrike", "bombing",
        ],
    },
    "Economic Intelligence": {
        "icon": "📊",
        "color": "#3b82f6",
        "keywords": [
            "economy", "gdp", "inflation", "interest rate", "central bank",
            "federal reserve", "monetary policy", "fiscal", "trade war", "tariff",
            "supply chain", "recession", "stock market", "commodity", "oil prices",
            "currency", "forex", "debt crisis", "imf", "world bank",
            "economic sanctions", "trade agreement", "export ban", "import duty",
        ],
    },
    "Climate & Environment": {
        "icon": "🌡️",
        "color": "#10b981",
        "keywords": [
            "climate change", "global warming", "carbon emissions", "renewable energy",
            "hurricane", "typhoon", "cyclone", "earthquake", "tsunami", "flood",
            "wildfire", "drought", "pollution", "deforestation", "biodiversity",
            "arctic", "sea level", "paris agreement", "cop", "net zero",
            "extreme weather", "heatwave", "tornado", "monsoon", "glacier",
        ],
    },
    "Technology & AI": {
        "icon": "🔬",
        "color": "#06b6d4",
        "keywords": [
            "artificial intelligence", "ai regulation", "machine learning",
            "quantum computing", "semiconductor", "chip", "5g", "6g",
            "space launch", "satellite", "spacex", "nasa", "isro",
            "blockchain", "cryptocurrency", "autonomous", "robotics",
            "biotech", "gene editing", "crispr", "neural network", "deepfake",
        ],
    },
    "Terrorism & Security": {
        "icon": "⚠️",
        "color": "#dc2626",
        "keywords": [
            "terrorism", "terrorist", "extremism", "radicalization", "insurgency",
            "bomb blast", "suicide attack", "hostage", "kidnapping", "assassination",
            "intelligence agency", "surveillance", "counter-terrorism", "isis",
            "al-qaeda", "security threat", "threat level", "border security",
            "organized crime", "cartel", "trafficking", "smuggling",
        ],
    },
    "Health & Pandemic": {
        "icon": "🏥",
        "color": "#ec4899",
        "keywords": [
            "pandemic", "epidemic", "outbreak", "virus", "vaccine", "who",
            "quarantine", "lockdown", "covid", "bird flu", "mpox",
            "public health", "disease", "infection", "mortality rate",
            "pharmaceutical", "clinical trial", "drug approval", "health crisis",
        ],
    },
    "Energy & Resources": {
        "icon": "⚡",
        "color": "#f59e0b",
        "keywords": [
            "oil", "gas", "opec", "energy crisis", "energy security", "pipeline",
            "lng", "natural gas", "petroleum", "crude oil", "refinery",
            "mining", "rare earth", "lithium", "cobalt", "uranium",
            "solar", "wind energy", "hydropower", "nuclear energy", "power grid",
        ],
    },
    "Maritime & Space": {
        "icon": "🚀",
        "color": "#6366f1",
        "keywords": [
            "maritime", "naval", "shipping lane", "strait", "port",
            "south china sea", "suez canal", "panama canal", "piracy",
            "space", "orbit", "launch", "asteroid", "moon mission",
            "mars", "space station", "starlink", "space debris", "rocket",
        ],
    },
}

# ── Hierarchical Region Detection ────────────────────────────────────────────
from backend.regions_data import HIERARCHICAL_REGION_MAP  # 30 countries

def _detect_location(text: str) -> tuple:
    """Returns (country_id, state_id, district_id) explicitly matched."""
    text_lower = f" {text.lower()} "
    
    best_country = None
    best_state = None
    best_district = None
    
    for country in HIERARCHICAL_REGION_MAP:
        c_match = any(kw in text_lower for kw in country["keywords"])
        for state in country.get("states", []):
            s_match = any(kw in text_lower for kw in state["keywords"])
            for dist in state.get("districts", []):
                d_match = any(kw in text_lower for kw in dist["keywords"])
                if d_match:
                    return (country["id"], state["id"], dist["id"])
            if s_match:
                best_country = country["id"]
                best_state = state["id"]
        if c_match and not best_country:
            best_country = country["id"]
            
    return (best_country, best_state, best_district)

def _detect_category(text: str) -> tuple:
    text_lower = text.lower()
    scores = {}
    for cat, info in INTEL_CATEGORIES.items():
        count = 0
        for kw in info["keywords"]:
            if kw in text_lower:
                count += 1
        if count > 0:
            scores[cat] = count
    if scores:
        best = max(scores, key=scores.get)
        return best, scores[best]
    return "Geopolitical", 0

def _generate_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()[:12]

def _assess_threat_level(title: str, desc: str) -> str:
    combined = (title + " " + desc).lower()
    critical_words = ["war", "attack", "nuclear", "invasion", "bombing", "terrorism", "crisis", "emergency", "catastrophe"]
    high_words = ["conflict", "sanctions", "missile", "threat", "breach", "escalat", "crash", "surge", "collapse"]
    medium_words = ["tension", "dispute", "concern", "warning", "risk", "alert", "volatile", "instability"]

    if any(w in combined for w in critical_words):
        return "Critical"
    if any(w in combined for w in high_words):
        return "High"
    if any(w in combined for w in medium_words):
        return "Medium"
    return "Low"

def _parse_time(time_str: str) -> str:
    if not time_str:
        return datetime.utcnow().isoformat() + "Z"
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return dt.isoformat()
    except Exception:
        pass
    try:
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"]:
            dt = datetime.strptime(time_str, fmt)
            return dt.isoformat()
    except Exception:
        pass
    return datetime.utcnow().isoformat() + "Z"

# ── API Fetchers ─────────────────────────────────────────────────────────────

def _fetch_gnews(query: str = "geopolitics OR military OR cybersecurity OR climate crisis") -> list:
    articles = []
    try:
        api_key = config.GNEWS_API_KEY
        if not api_key:
            return []
        url = "https://gnews.io/api/v4/search"
        params = {"q": query, "lang": "en", "max": 50, "sortby": "publishedAt", "apikey": api_key}
        resp = requests.get(url, params=params, timeout=8)
        if resp.status_code == 200:
            for item in resp.json().get("articles", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "source": item.get("source", {}).get("name", "GNews"),
                    "url": item.get("url", ""),
                    "image": item.get("image", ""),
                    "published_at": _parse_time(item.get("publishedAt", "")),
                    "api_source": "GNews",
                })
    except Exception:
        pass
    return articles

def _fetch_newsdata(query: str = "geopolitics OR military OR cybersecurity") -> list:
    articles = []
    try:
        api_key = config.NEWSDATA_API_KEY
        if not api_key:
            return []
        url = "https://newsdata.io/api/1/latest"
        params = {"apikey": api_key, "q": query, "language": "en", "size": 30}
        resp = requests.get(url, params=params, timeout=8)
        if resp.status_code == 200:
            for item in resp.json().get("results", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", "") or item.get("content", "") or "",
                    "source": item.get("source_name", "NewsData"),
                    "url": item.get("link", ""),
                    "image": item.get("image_url", ""),
                    "published_at": _parse_time(item.get("pubDate", "")),
                    "api_source": "NewsData.io",
                })
    except Exception:
        pass
    return articles

def _fetch_newsapi(query: str = "geopolitics OR defense OR cybersecurity") -> list:
    articles = []
    try:
        api_key = config.NEWSAPI_KEY
        if not api_key:
            return []
        url = "https://newsapi.org/v2/everything"
        params = {"q": query, "language": "en", "sortBy": "publishedAt", "pageSize": 50, "apiKey": api_key}
        resp = requests.get(url, params=params, timeout=8)
        if resp.status_code == 200:
            for item in resp.json().get("articles", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", "") or "",
                    "source": item.get("source", {}).get("name", "NewsAPI"),
                    "url": item.get("url", ""),
                    "image": item.get("urlToImage", ""),
                    "published_at": _parse_time(item.get("publishedAt", "")),
                    "api_source": "NewsAPI",
                })
    except Exception:
        pass
    return articles

def _fetch_gdelt(query: str = "geopolitics OR military OR cybersecurity OR climate crisis") -> list:
    articles = []
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {"query": query, "mode": "ArtList", "maxrecords": 50, "format": "json", "sort": "DateDesc"}
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            for item in resp.json().get("articles", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("seendate", ""),
                    "source": item.get("domain", "GDELT"),
                    "url": item.get("url", ""),
                    "image": item.get("socialimage", ""),
                    "published_at": _parse_time(item.get("seendate", "")),
                    "api_source": "GDELT",
                })
    except Exception:
        pass
    return articles

def _fetch_currents(query: str = "geopolitics") -> list:
    articles = []
    try:
        api_key = config.__dict__.get("CURRENTS_API_KEY", "") or ""
        if not api_key:
            import os
            api_key = os.getenv("CURRENTS_API_KEY", "")
        if not api_key:
            return []
        url = "https://api.currentsapi.services/v1/search"
        params = {"keywords": query, "language": "en", "limit": 40, "apiKey": api_key}
        resp = requests.get(url, params=params, timeout=8)
        if resp.status_code == 200:
            for item in resp.json().get("news", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("description", ""),
                    "source": item.get("author", "Currents"),
                    "url": item.get("url", ""),
                    "image": item.get("image", ""),
                    "published_at": _parse_time(item.get("published", "")),
                    "api_source": "Currents",
                })
    except Exception:
        pass
    return articles

def _fetch_worldnews(query: str = "geopolitics") -> list:
    articles = []
    try:
        api_key = config.WORLDNEWS_API_KEY
        if not api_key:
            return []
        url = "https://api.worldnewsapi.com/search-news"
        params = {"text": query, "language": "en", "sort": "publish-time", "sort-direction": "DESC", "number": 30, "api-key": api_key}
        resp = requests.get(url, params=params, timeout=8)
        if resp.status_code == 200:
            for item in resp.json().get("news", []):
                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("text", "")[:300] if item.get("text") else "",
                    "source": item.get("source_country", "WorldNews") or "WorldNews",
                    "url": item.get("url", ""),
                    "image": item.get("image", ""),
                    "published_at": _parse_time(item.get("publish_date", "")),
                    "api_source": "WorldNews",
                })
    except Exception:
        pass
    return articles


def _fetch_rss(feed_urls: list, limit_per_feed=5) -> list:
    articles = []
    try:
        def fetch_single(url):
            res = []
            try:
                parsed = feedparser.parse(url)
                for entry in parsed.entries[:limit_per_feed]:
                    res.append({
                        "title": entry.get("title", ""),
                        "description": entry.get("summary", ""),
                        "source": parsed.feed.get("title", "RSS"),
                        "url": entry.get("link", ""),
                        "image": "",
                        "published_at": _parse_time(entry.get("published", "")),
                        "api_source": "RSS",
                    })
            except Exception:
                pass
            return res
        
        with ThreadPoolExecutor(max_workers=10) as ex:
            futs = [ex.submit(fetch_single, u) for u in feed_urls]
            for f in as_completed(futs, timeout=10):
                res = f.result(timeout=10)
                if res: articles.extend(res)
    except Exception:
        pass
    return articles

# ── Cache ────────────────────────────────────────────────────────────────────
_cache = {"data": None, "timestamp": 0, "ttl": 30} # Reduced to 30 seconds for real-time fetching

def _extract_keywords(text: str) -> list:
    text_lower = text.lower()
    found = []
    all_kws = []
    for cat, info in INTEL_CATEGORIES.items():
        all_kws.extend(info["keywords"])

    for kw in all_kws:
        if kw in text_lower and kw not in found:
            found.append(kw)
            if len(found) >= 5:
                break
    return found

def _clean_text(text: str) -> str:
    if not text: return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Strip markdown links
    clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
    # Drop loose links to keep UI clean
    clean = re.sub(r'https?://[^\s]+', '', clean)
    # Clean up excess whitespace
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

_TRANSLATION_CACHE = {}

def _translate_to_english(text: str) -> str:
    if not text or len(text.strip()) < 3:
        return text
    
    if text in _TRANSLATION_CACHE:
        return _TRANSLATION_CACHE[text]

    # Fast heuristic check for English: skip network translation if basic English words found
    lower_text = text.lower()
    common_english = {"the", "and", "to", "of", "a", "in", "for", "is", "on", "that", "by", "this", "with", "are", "be"}
    words = set(re.findall(r'\b[a-z]+\b', lower_text))
    # Note: Using 2 or more common words to definitively spot English
    if len(words.intersection(common_english)) >= 2:
        _TRANSLATION_CACHE[text] = text
        return text

    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(text[:4000])
        final = translated if translated else text
        _TRANSLATION_CACHE[text] = final
        return final
    except Exception as e:
        logger.warning(f"Translation failed for '{text[:20]}': {e}")
        return text

def _enrich_article(article: dict) -> dict:
    """Add category, location hierarchy, threat level, and sentiment to an article."""
    title = _clean_text(str(article.get("title", "")))
    desc = _clean_text(str(article.get("description", "")))
    
    # Fast Translate: Convert non-English context to English
    # Note: `deep-translator` auto-detects language. It's fast and handles Spanish, etc.
    if title:
        title = _translate_to_english(title)
        article["title"] = title
    if desc:
        desc = _translate_to_english(desc)
        article["description"] = desc
        
    combined = title + " " + desc

    category, score = _detect_category(combined)
    c_id, s_id, d_id = _detect_location(combined)
    threat = _assess_threat_level(title, desc)

    article["id"] = _generate_id(title + str(article.get("url", "")))
    article["category"] = category
    article["category_icon"] = INTEL_CATEGORIES.get(category, {}).get("icon", "📰")
    article["category_color"] = INTEL_CATEGORIES.get(category, {}).get("color", "#6b7280")
    article["country_id"] = c_id
    article["state_id"] = s_id
    article["district_id"] = d_id
    
    sentiment_map = {"Critical": ("Negative", 85.5), "High": ("Negative", 72.1), "Medium": ("Neutral", 50.5), "Low": ("Positive", 80.0)}
    sentiment, sentiment_score = sentiment_map.get(threat, ("Neutral", 50))
    article["sentiment"] = sentiment
    article["score"] = str(sentiment_score)
    article["time"] = article.get("published_at", "")
    
    article["summary"] = desc[:200] + "..." if desc else "No description available."
    
    article["threat_level"] = threat
    article["relevance_score"] = min(score * 15 + 30, 100)
    article["keywords"] = _extract_keywords(combined)

    # DOMINANCE LOGIC: Massive boost for India and Tamil Nadu
    if c_id == "ind":
        article["relevance_score"] += 500
    if s_id == "in_tn":
        article["relevance_score"] += 1000

    return article

def fetch_geo_intelligence(query: str = None) -> dict:
    import copy
    now = time.time()

    # Use cache if available and not expired for the default global view
    if not query and _cache["data"] and (now - _cache["timestamp"]) < _cache["ttl"]:
        logger.info("Serving Geo-Intelligence from cache.")
        return _cache["data"]

    logger.info("Fetching fresh geo-intelligence. (Priority: India & Tamil Nadu)")

    all_articles = []
    live_articles = []
    
    # Prioritize India and Tamil Nadu briefly
    priority_queries = [
        "tamil nadu OR chennai OR india geopolitics"
    ]
    
    # Global coverage broadly
    global_queries = [
        "geopolitics OR cyberattack OR climate emergency"
    ]
    
    all_q = priority_queries + global_queries
    if query:
        all_q = [query]

    # Increase max_workers to run faster in parallel, set smaller timeout
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for q in all_q:
            futures.append(executor.submit(_fetch_gnews, q))
            futures.append(executor.submit(_fetch_newsdata, q))
            if not query: # general fetch
                futures.append(executor.submit(_fetch_newsapi, q))

        try:
            for future in as_completed(futures, timeout=6):
                try:
                    res = future.result(timeout=6)
                    if res: live_articles.extend(res)
                except Exception:
                    pass
        except Exception:
            pass
        
        # Always try to supplement with RSS for regional dominance
        if not query:
            try:
                rss_res = _fetch_rss(config.RSS_FEEDS[:30])
                if rss_res: live_articles.extend(rss_res)
            except Exception:
                pass

    # ── Scraper Fallback: if APIs returned very little, scrape directly ──
    if len(live_articles) < 5:
        logger.info("API sources returned < 5 articles. Activating web scraper fallback.")
        try:
            from backend.scraper_fallback import scrape_fallback_news
            scraped = scrape_fallback_news()
            if scraped:
                live_articles.extend(scraped)
                logger.info("Scraper fallback added %d articles.", len(scraped))
        except Exception as e:
            logger.warning("Scraper fallback failed: %s", e)

    try:
        db_articles = database.get_recent_articles(300)
    except Exception as e:
        logger.error("DB Fetch error: %s", e)
        db_articles = []

    # Get seen normalized titles from DB to prevent saving duplicates
    db_seen_titles = set()
    for a in db_articles:
        if "source" not in a: a["source"] = "Database"
        a["published_at"] = a.get("published_at", "")
        a["api_source"] = "Database"
        t = str(a.get("title", "")).strip()
        if len(t) >= 10:
            db_seen_titles.add(re.sub(r'[^a-z0-9]', '', t.lower())[:60])
        all_articles.append(a)

    new_to_save = []
    live_seen_titles = set()
    for a in live_articles:
        t = str(a.get("title", "")).strip()
        if len(t) < 10: continue
        norm = re.sub(r'[^a-z0-9]', '', t.lower())[:60]
        if norm not in db_seen_titles and norm not in live_seen_titles:
            live_seen_titles.add(norm)
            new_to_save.append(a)
            all_articles.append(a)
    
    if new_to_save:
        try:
            database.save_articles(new_to_save, pipeline_run_id="geo_live_fetch")
        except Exception: pass

    # Fully deduplicate all merged articles
    seen = set()
    unique = []
    for a in all_articles:
        title = str(a.get("title", "")).strip()
        if len(title) < 10: continue
        norm = re.sub(r'[^a-z0-9]', '', title.lower())[:60]
        if norm not in seen:
            seen.add(norm)
            unique.append(a)

    # Parallel enrichment since translation and logic can be slow
    with ThreadPoolExecutor(max_workers=20) as executor:
        enriched = list(executor.map(_enrich_article, unique))
        
    enriched.sort(key=lambda x: (x.get("relevance_score", 0), x.get("time", "")), reverse=True)

    all_keywords = set()
    for cat_info in INTEL_CATEGORIES.values():
        all_keywords.update(cat_info["keywords"][:5])
    
    regions_output = copy.deepcopy(HIERARCHICAL_REGION_MAP)

    for country in regions_output:
        c_news = [a for a in enriched if a.get("country_id") == country["id"]]
        country["news"] = sorted(c_news, key=lambda x: x.get("relevance_score", 0), reverse=True)[:50]
        for state in country.get("states", []):
            s_news = [a for a in enriched if a.get("state_id") == state["id"]]
            state["news"] = sorted(s_news, key=lambda x: x.get("relevance_score", 0), reverse=True)[:30]
            for dist in state.get("districts", []):
                d_news = [a for a in enriched if a.get("district_id") == dist["id"]]
                dist["news"] = sorted(d_news, key=lambda x: x.get("relevance_score", 0), reverse=True)[:20]

    global_news = [a for a in enriched if not a.get("country_id")]
    if global_news:
        regions_output.insert(0, {
            "id": "global_hub",
            "name": "Global Surveillance Hub",
            "code": "GL",
            "news": sorted(global_news, key=lambda x: x.get("relevance_score", 0), reverse=True)[:100],
            "states": []
        })

    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_articles": len(enriched),
        "api_sources": list(set(a.get("api_source", "Unknown") for a in enriched)),
        "keywords": list(all_keywords)[:40],
        "regions": regions_output,
        "query": query
    }

    if not query:
        _cache["data"] = result
        _cache["timestamp"] = now

    return result

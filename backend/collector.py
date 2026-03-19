"""
VEILORACLE — News Collector
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Multi-tier collection: NewsData.io → GDELT Raw Files → RSS → sample data.
"""

import logging
import requests
import csv
import io
import zipfile
from datetime import datetime, timedelta

import feedparser

from backend import config

logger = logging.getLogger("veiloracle.collector")

def fetch_from_newsdata() -> list[dict]:
    """Fetch from newsdata.io API - ACTIVE PRIMARY SOURCE."""
    if not config.NEWSDATA_API_KEY:
        logger.info("No NEWSDATA_API_KEY — skipping newsdata.io.")
        return []
    try:
        # Note: free tier uses 'size' not 'max_results'
        url = f"https://newsdata.io/api/1/latest?apikey={config.NEWSDATA_API_KEY}&language=en&size=50"
        response = requests.get(url, timeout=12)
        if response.status_code == 422:
            # Fallback: try without size param
            url = f"https://newsdata.io/api/1/latest?apikey={config.NEWSDATA_API_KEY}&language=en"
            response = requests.get(url, timeout=12)
        if response.status_code == 429:
            logger.warning("✗ Newsdata.io rate limited — skipping")
            return []
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "success":
            logger.warning("✗ Newsdata.io error: %s", data.get("results", {}).get("message", "unknown"))
            return []
        articles = []
        for raw in data.get("results", []):
            if not raw.get("title"):
                continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("description") or "",
                "source": raw.get("source_id", "newsdata"),
                "url": raw.get("link", ""),
                "published_at": raw.get("pubDate", datetime.utcnow().isoformat())
            })
        logger.info("✓ Newsdata.io: %d articles fetched", len(articles))
        return articles
    except Exception as e:
        logger.warning("✗ Newsdata.io failed: %s", e)
        return []

def fetch_from_gdelt_rawfiles(max_articles: int = 50) -> list[dict]:
    """Fetch real-time news from GDELT API.
    
    Capped to max_articles to prevent dominating the feed.
    GDELT is free and always available, so we use it as a supplementary source.
    """
    import time as _time
    articles = []
    try:
        gdelt_url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "news",
            "mode": "ArtList",
            "maxrecords": max_articles,
            "format": "json",
            "sort": "date"
        }
        
        response = requests.get(gdelt_url, params=params, timeout=15)
        
        # Handle rate limiting with a single retry
        if response.status_code == 429:
            logger.warning("GDELT rate-limited (429), waiting 5s and retrying...")
            _time.sleep(5)
            response = requests.get(gdelt_url, params=params, timeout=15)
            if response.status_code == 429:
                logger.warning("✗ GDELT still rate-limited — skipping")
                return []
        
        response.raise_for_status()
        data = response.json()
        
        for raw in data.get("articles", []):
            title = raw.get("title", "") or raw.get("url", "")
            url = raw.get("url", "")
            source = raw.get("source", "GDELT")
            
            if title and len(title) > 10:
                articles.append({
                    "title": title[:200].strip(),
                    "description": raw.get("snippet", ""),
                    "source": source,
                    "url": url,
                    "published_at": datetime.utcnow().isoformat()
                })
        
        logger.info(f"✓ GDELT API: {len(articles)} articles fetched (capped at {max_articles})")
        return articles
        
    except Exception as e:
        logger.warning(f"✗ GDELT API failed: {e}")
        return []


def fetch_from_rss(max_per_feed: int = 15) -> list[dict]:
    """Parse RSS feeds. No API key required. Handles timeouts gracefully."""
    articles = []
    for feed_url in config.RSS_FEEDS:
        try:
            # Use custom timeout and retry logic
            feed = feedparser.parse(feed_url, timeout=5)  # 5 second timeout
            
            # Check if feed parsing was successful
            if not feed.entries:
                logger.debug(f"RSS feed empty: {feed_url}")
                continue
                
            feed_name = feed.feed.get("title", feed_url)
            for entry in feed.entries[:max_per_feed]:
                pub_date = entry.get("published", datetime.utcnow().isoformat())
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        pub_date = datetime(*entry.published_parsed[:6]).isoformat()
                    except Exception:
                        pass
                articles.append({
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", entry.get("description", "")),
                    "source": feed_name,
                    "url": entry.get("link", ""),
                    "published_at": pub_date,
                })
            logger.info(f"✓ RSS [{feed_name[:40]}]: {min(len(feed.entries), max_per_feed)} articles")
            
        except Exception as e:
            logger.debug(f"RSS timeout/failed ({feed_url[:50]}): {type(e).__name__}")
            continue
            
    return articles


def fetch_from_newsapi(category: str = "general", page_size: int = 20) -> list[dict]:
    if not config.NEWSAPI_KEY: return []
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize={page_size}&apiKey={config.NEWSAPI_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        articles = []
        for raw in data.get("articles", []):
            if not raw.get("title") or raw["title"] == "[Removed]": continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("description") or "",
                "source": raw.get("source", {}).get("name", "NewsAPI"),
                "url": raw.get("url", ""),
                "published_at": raw.get("publishedAt", datetime.utcnow().isoformat()),
            })
        logger.info("✓ NewsAPI [%s]: %d articles", category, len(articles))
        return articles
    except Exception as e:
        logger.warning("✗ NewsAPI failed: %s", e)
        return []

def fetch_from_gnews() -> list[dict]:
    if not config.GNEWS_API_KEY: return []
    articles = []
    categories = ["general", "world", "business", "technology"]
    for cat in categories:
        try:
            url = f"https://gnews.io/api/v4/top-headlines?category={cat}&lang=en&max=20&apikey={config.GNEWS_API_KEY}"
            response = requests.get(url, timeout=10)
            if response.status_code == 403 or response.status_code == 429: break
            data = response.json()
            for raw in data.get("articles", []):
                if not raw.get("title"): continue
                articles.append({
                    "title": raw["title"],
                    "description": raw.get("description") or "",
                    "source": raw.get("source", {}).get("name", "GNews"),
                    "url": raw.get("url", ""),
                    "published_at": raw.get("publishedAt", datetime.utcnow().isoformat())
                })
        except Exception: pass
    logger.info("✓ GNews: %d articles", len(articles))
    return articles

def fetch_from_worldnews() -> list[dict]:
    if not config.WORLDNEWS_API_KEY: return []
    try:
        url = f"https://api.worldnewsapi.com/search-news?text=news&language=en&number=50&api-key={config.WORLDNEWS_API_KEY}"
        response = requests.get(url, timeout=12)
        if response.status_code != 200: return []
        data = response.json()
        articles = []
        for raw in data.get("news", []):
            if not raw.get("title"): continue
            articles.append({
                "title": raw["title"],
                "description": (raw.get("text") or "")[:500],
                "source": raw.get("source", "WorldNewsAPI"),
                "url": raw.get("url", ""),
                "published_at": raw.get("publish_date", datetime.utcnow().isoformat())
            })
        logger.info("✓ WorldNews: %d articles fetched", len(articles))
        return articles
    except Exception: return []

def fetch_from_webz() -> list[dict]:
    if not config.WEBZ_API_KEY: return []
    try:
        url = f"https://api.webz.io/newsApiLite?token={config.WEBZ_API_KEY}&q=news"
        response = requests.get(url, timeout=10)
        data = response.json()
        articles = []
        for raw in data.get("posts", []):
            if not raw.get("title"): continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("text") or "",
                "source": raw.get("thread", {}).get("site", "Webz.io"),
                "url": raw.get("url", ""),
                "published_at": raw.get("published", datetime.utcnow().isoformat())
            })
        logger.info("✓ Webz.io: %d articles", len(articles))
        return articles
    except Exception: return []


def fetch_sample_data() -> list[dict]:
    """Return built-in sample articles for offline mode."""
    logger.info("Using %d sample articles (offline mode)", len(config.SAMPLE_ARTICLES))
    return list(config.SAMPLE_ARTICLES)


def collect_news() -> list[dict]:
    """Multi-tier collection from ALL configured API sources.
    
    Fetches from every available API key in parallel priority order.
    Always returns a non-empty, deduplicated list.
    """
    source_counts = {}  # Track how many articles each source contributed
    articles = []
    
    def _extend(name, fetched):
        source_counts[name] = len(fetched)
        articles.extend(fetched)
    
    # ── PRIMARY PAID APIs (highest priority, richest data) ────────
    logger.info("━" * 50)
    logger.info("▸ [1/8] GNews API...")
    _extend("GNews", fetch_from_gnews())
    
    logger.info("▸ [2/8] NewsData.io API...")
    _extend("Newsdata.io", fetch_from_newsdata())
    
    logger.info("▸ [3/8] WorldNews API...")
    _extend("WorldNews", fetch_from_worldnews())
    
    logger.info("▸ [4/8] Webz.io API...")
    _extend("Webz.io", fetch_from_webz())
    
    # ── SECONDARY APIs ────────────────────────────────────────────
    logger.info("▸ [5/8] NewsAPI (multi-category)...")
    if config.NEWSAPI_KEY:
        newsapi_all = []
        for cat in config.NEWS_CATEGORIES:
            newsapi_all.extend(fetch_from_newsapi(category=cat, page_size=20))
        _extend("NewsAPI", newsapi_all)
    else:
        source_counts["NewsAPI"] = 0
    
    # ── FREE / SUPPLEMENTARY SOURCES (capped to avoid flooding) ──
    logger.info("▸ [6/8] GDELT (supplementary)...")
    _extend("GDELT", fetch_from_gdelt_rawfiles(max_articles=50))
    
    logger.info("▸ [7/8] RSS Feeds (massive multi-domain)...")
    _extend("RSS", fetch_from_rss(max_per_feed=20))
        
    # ── FALLBACK ──────────────────────────────────────────────────
    if not articles:
        logger.warning("▸ No real data from any source — using sample articles")
        articles = fetch_sample_data()
        source_counts["Sample"] = len(articles)
    
    # ── DEDUPLICATION ─────────────────────────────────────────────
    seen, unique = set(), []
    for a in articles:
        key = a.get("title", "").strip().lower()
        if key and len(key) > 5 and key not in seen:
            seen.add(key)
            unique.append(a)
    
    # ── SOURCE BREAKDOWN REPORT ──────────────────────────────────
    logger.info("━" * 50)
    logger.info("📊 SOURCE COLLECTION BREAKDOWN:")
    for src, cnt in sorted(source_counts.items(), key=lambda x: -x[1]):
        bar = "█" * min(cnt, 40)
        status = "✓" if cnt > 0 else "✗"
        logger.info("  %s %-14s %3d articles  %s", status, src, cnt, bar)
    logger.info("  ─────────────────────────────────")
    logger.info("  Total raw: %d | After dedup: %d", len(articles), len(unique))
    logger.info("━" * 50)
    
    return unique

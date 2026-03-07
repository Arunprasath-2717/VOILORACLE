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


def fetch_from_newsapi(category: str = "general", page_size: int = None) -> list[dict]:
    """Fetch top headlines from NewsAPI free tier."""
    if not config.NEWSAPI_KEY:
        logger.info("No NEWSAPI_KEY — skipping NewsAPI.")
        return []
    try:
        from newsapi import NewsApiClient
        api = NewsApiClient(api_key=config.NEWSAPI_KEY)
        page_size = page_size or config.MAX_ARTICLES_PER_FETCH
        response = api.get_top_headlines(category=category, country=config.NEWS_COUNTRY, page_size=page_size)
        if response.get("status") != "ok":
            return []
        articles = []
        for raw in response.get("articles", []):
            if not raw.get("title") or raw["title"] == "[Removed]":
                continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("description") or "",
                "source": raw.get("source", {}).get("name", "Unknown"),
                "url": raw.get("url", ""),
                "published_at": raw.get("publishedAt", datetime.utcnow().isoformat()),
            })
        logger.info("NewsAPI: %d articles (category=%s)", len(articles), category)
        return articles
    except Exception as e:
        logger.error("NewsAPI failed: %s", e)
        return []

def fetch_from_newsdata() -> list[dict]:
    """Fetch from newsdata.io API - ACTIVE PRIMARY SOURCE."""
    if not config.NEWSDATA_API_KEY:
        logger.info("No NEWSDATA_API_KEY — skipping newsdata.io.")
        return []
    try:
        url = f"https://newsdata.io/api/1/news?apikey={config.NEWSDATA_API_KEY}&language=en&max_results=50"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
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
        logger.warning("Newsdata.io failed: %s", e)
        return []

def fetch_from_gdelt_rawfiles() -> list[dict]:
    """Fetch real-time news from GDELT API (fallback from raw files).
    
    GDELT API is simpler and more reliable than raw file parsing.
    """
    articles = []
    try:
        # Use GDELT API directly
        gdelt_url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "news",
            "mode": "ArtList",
            "maxrecords": 50,
            "format": "json",
            "sort": "date"
        }
        
        response = requests.get(gdelt_url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract articles from GDELT API response
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
        
        if articles:
            logger.info(f"✓ GDELT API: {len(articles)} articles fetched")
        return articles
        
    except Exception as e:
        logger.warning(f"GDELT API failed: {e}")
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


def fetch_from_gnews() -> list[dict]:
    """Fetch from GNews API."""
    if not config.GNEWS_API_KEY:
        logger.info("No GNEWS_API_KEY — skipping GNews.")
        return []
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&apikey={config.GNEWS_API_KEY}&max=50"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for raw in data.get("articles", []):
            if not raw.get("title"):
                continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("description") or "",
                "source": raw.get("source", {}).get("name", "GNews"),
                "url": raw.get("url", ""),
                "published_at": raw.get("publishedAt", datetime.utcnow().isoformat())
            })
        logger.info("✓ GNews: %d articles fetched", len(articles))
        return articles
    except Exception as e:
        logger.warning("GNews failed: %s", e)
        return []


def fetch_from_worldnews() -> list[dict]:
    """Fetch from WorldNews API."""
    if not config.WORLDNEWS_API_KEY:
        logger.info("No WORLDNEWS_API_KEY — skipping WorldNews.")
        return []
    try:
        url = f"https://api.worldnewsapi.com/search-news?text=news&language=en&api-key={config.WORLDNEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for raw in data.get("news", []):
            if not raw.get("title"):
                continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("text") or "",
                "source": raw.get("source", "WorldNewsAPI"),
                "url": raw.get("url", ""),
                "published_at": raw.get("publish_date", datetime.utcnow().isoformat())
            })
        logger.info("✓ WorldNews: %d articles fetched", len(articles))
        return articles
    except Exception as e:
        logger.warning("WorldNews failed: %s", e)
        return []


def fetch_from_thenews() -> list[dict]:
    """Fetch from TheNews API."""
    if not config.THENEWS_API_KEY:
        logger.info("No THENEWS_API_KEY — skipping TheNews.")
        return []
    try:
        url = f"https://api.thenewsapi.com/v1/news/top?api_token={config.THENEWS_API_KEY}&locale=us&language=en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for raw in data.get("data", []):
            if not raw.get("title"):
                continue
            articles.append({
                "title": raw["title"],
                "description": raw.get("description") or "",
                "source": raw.get("source", "TheNewsAPI"),
                "url": raw.get("url", ""),
                "published_at": raw.get("published_at", datetime.utcnow().isoformat())
            })
        logger.info("✓ TheNews: %d articles fetched", len(articles))
        return articles
    except Exception as e:
        logger.warning("TheNews failed: %s", e)
        return []


def fetch_from_webz() -> list[dict]:
    """Fetch from Webz.io News API Lite."""
    if not config.WEBZ_API_KEY:
        logger.info("No WEBZ_API_KEY — skipping Webz.io.")
        return []
    try:
        url = f"https://api.webz.io/newsApiLite?token={config.WEBZ_API_KEY}&q=news"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for raw in data.get("posts", []):
            if not raw.get("title"):
                continue
            source_name = raw.get("thread", {}).get("site", "Webz.io")
            articles.append({
                "title": raw["title"],
                "description": raw.get("text") or "",
                "source": source_name,
                "url": raw.get("url", ""),
                "published_at": raw.get("published", datetime.utcnow().isoformat())
            })
        logger.info("✓ Webz.io: %d articles fetched", len(articles))
        return articles
    except Exception as e:
        logger.warning("Webz.io failed: %s", e)
        return []



def fetch_sample_data() -> list[dict]:
    """Return built-in sample articles for offline mode."""
    logger.info("Using %d sample articles (offline mode)", len(config.SAMPLE_ARTICLES))
    return list(config.SAMPLE_ARTICLES)


def collect_news() -> list[dict]:
    """Multi-tier collection. Always returns non-empty list."""
    articles = []
    
    # 1. GNews API (New Primary Source)
    logger.info("▸ Fetching from GNews...")
    articles.extend(fetch_from_gnews())
    
    # 2. WorldNews API
    logger.info("▸ Fetching from WorldNews API...")
    articles.extend(fetch_from_worldnews())
    
    # 3. TheNews API
    logger.info("▸ Fetching from TheNews API...")
    articles.extend(fetch_from_thenews())
    
    # 4. Webz.io API
    logger.info("▸ Fetching from Webz.io API...")
    articles.extend(fetch_from_webz())
    
    # 5. Newsdata.io 
    logger.info("▸ Fetching from Newsdata.io...")
    articles.extend(fetch_from_newsdata())
    
    # 6. GDELT Raw Data Files (Global Event Database)
    logger.info("▸ Fetching from GDELT raw files...")
    articles.extend(fetch_from_gdelt_rawfiles())
    
    # 7. NewsAPI (if key available)
    if config.NEWSAPI_KEY:
        logger.info("▸ Fetching from NewsAPI...")
        for cat in config.NEWS_CATEGORIES:
            articles.extend(fetch_from_newsapi(category=cat))
            
    # 8. RSS Feeds (always fallback if needed)
    if len(articles) < 40:
        logger.info("▸ Fetching from RSS feeds (fallback)...")
        articles.extend(fetch_from_rss(max_per_feed=10))
        
    # 5. Sample data (last resort)
    if not articles:
        logger.warning("▸ No real data available, using sample articles...")
        articles = fetch_sample_data()
    
    # Deduplicate by title
    seen, unique = set(), []
    for a in articles:
        key = a.get("title", "").strip().lower()
        if key and len(key) > 5 and key not in seen:
            seen.add(key)
            unique.append(a)
    
    logger.info(f"✓ Collector: {len(unique)} unique articles collected from {len(articles)} total.")
    return unique

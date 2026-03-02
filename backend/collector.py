"""
VEILORACLE — News Collector
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Three-tier collection: NewsAPI → RSS → sample data.
"""

import logging
import requests
from datetime import datetime

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
    """Fetch from newsdata.io API."""
    if not config.NEWSDATA_API_KEY:
        logger.info("No NEWSDATA_API_KEY — skipping newsdata.io.")
        return []
    try:
        url = f"https://newsdata.io/api/1/news?apikey={config.NEWSDATA_API_KEY}&language=en"
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
        logger.info("Newsdata.io: %d articles", len(articles))
        return articles
    except Exception as e:
        logger.error("Newsdata.io failed: %s", e)
        return []

def fetch_from_gdelt() -> list[dict]:
    """Fetch real-time news from GDELT."""
    try:
        response = requests.get(config.GDELT_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for raw in data.get("articles", []):
            if not raw.get("title"):
                continue
            articles.append({
                "title": raw["title"],
                "description": "",
                "source": raw.get("domain", "GDELT"),
                "url": raw.get("url", ""),
                "published_at": raw.get("seendate", datetime.utcnow().isoformat())
            })
        logger.info("GDELT: %d articles", len(articles))
        return articles
    except Exception as e:
        logger.error("GDELT failed: %s", e)
        return []


def fetch_from_rss(max_per_feed: int = 15) -> list[dict]:
    """Parse RSS feeds. No API key required."""
    articles = []
    for feed_url in config.RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
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
            logger.info("RSS [%s]: %d articles", feed_name, min(len(feed.entries), max_per_feed))
        except Exception as e:
            logger.warning("RSS failed (%s): %s", feed_url, e)
    return articles


def fetch_sample_data() -> list[dict]:
    """Return built-in sample articles for offline mode."""
    logger.info("Using %d sample articles (offline mode)", len(config.SAMPLE_ARTICLES))
    return list(config.SAMPLE_ARTICLES)


def collect_news() -> list[dict]:
    """Multi-tier collection. Always returns non-empty list."""
    articles = []
    
    # 1. Newsdata.io
    articles.extend(fetch_from_newsdata())
    
    # 2. GDELT
    articles.extend(fetch_from_gdelt())
    
    # 3. NewsAPI
    if config.NEWSAPI_KEY:
        for cat in config.NEWS_CATEGORIES:
            articles.extend(fetch_from_newsapi(category=cat))
            
    # 4. RSS Feeds (always fallback)
    if len(articles) < 50:
        articles.extend(fetch_from_rss())
        
    if not articles:
        articles = fetch_sample_data()
    # Deduplicate
    seen, unique = set(), []
    for a in articles:
        key = a["title"].strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(a)
    logger.info("Collector: %d unique articles ready.", len(unique))
    return unique

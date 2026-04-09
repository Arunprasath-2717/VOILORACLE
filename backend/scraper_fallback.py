"""
Kronaxis — Web Scraping Fallback Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When all third-party APIs hit rate limits or fail,
this module scrapes news directly from public RSS/HTML sources.
"""

import logging
import hashlib
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

logger = logging.getLogger("Kronaxis.scraper_fallback")

# Top-tier, always-available public news pages
SCRAPE_TARGETS = [
    {
        "name": "BBC World",
        "url": "https://www.bbc.com/news/world",
        "selector": "h3",
        "link_parent": "a",
        "base_url": "https://www.bbc.com",
    },
    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/news",
        "selector": "h3.article-card__title",
        "link_parent": "a",
        "base_url": "https://www.aljazeera.com",
    },
    {
        "name": "Reuters World",
        "url": "https://www.reuters.com/world/",
        "selector": "h3",
        "link_parent": "a",
        "base_url": "https://www.reuters.com",
    },
    {
        "name": "The Hindu India",
        "url": "https://www.thehindu.com/news/national/",
        "selector": "h3.title",
        "link_parent": "a",
        "base_url": "https://www.thehindu.com",
    },
    {
        "name": "NDTV India",
        "url": "https://www.ndtv.com/india-news",
        "selector": "h2.newsHdng",
        "link_parent": "a",
        "base_url": "https://www.ndtv.com",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _generate_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()[:12]


def _scrape_single(target: dict, limit: int = 15) -> list:
    """Scrape headlines from a single news outlet."""
    articles = []
    try:
        resp = requests.get(target["url"], headers=HEADERS, timeout=6)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        headlines = soup.select(target["selector"])

        seen = set()
        for h in headlines[:limit]:
            title = h.get_text(strip=True)
            if not title or len(title) < 15:
                continue

            # Deduplicate within this scrape
            norm = re.sub(r'[^a-z0-9]', '', title.lower())[:60]
            if norm in seen:
                continue
            seen.add(norm)

            # Try to find the parent link
            link = ""
            parent_a = h.find_parent("a")
            if parent_a and parent_a.get("href"):
                href = parent_a["href"]
                if href.startswith("/"):
                    link = target["base_url"] + href
                elif href.startswith("http"):
                    link = href

            articles.append({
                "id": _generate_id(title),
                "title": title,
                "description": "",
                "source": target["name"],
                "url": link,
                "image": "",
                "published_at": datetime.utcnow().isoformat() + "Z",
                "api_source": "Scraper",
            })
    except Exception as e:
        logger.warning("Scrape failed for %s: %s", target["name"], e)

    return articles


def scrape_fallback_news(max_per_source: int = 15) -> list:
    """
    Scrape headlines from all configured news outlets in parallel.
    Returns a flat list of article dicts.
    """
    all_articles = []

    with ThreadPoolExecutor(max_workers=len(SCRAPE_TARGETS)) as executor:
        futures = {
            executor.submit(_scrape_single, t, max_per_source): t["name"]
            for t in SCRAPE_TARGETS
        }

        try:
            for future in as_completed(futures, timeout=8):
                try:
                    result = future.result(timeout=8)
                    if result:
                        all_articles.extend(result)
                except Exception:
                    pass
        except Exception:
            pass

    logger.info("Scraper fallback collected %d articles from %d sources.",
                len(all_articles), len(SCRAPE_TARGETS))
    return all_articles

"""
VEILORACLE — Supabase Database Ingestion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Safely inserts processed articles into Supabase, managing deduplication (title + source)
and centralized system logging.
"""

import logging
from typing import Dict, Any, List
from backend.supabase_client import get_supabase_client
from datetime import datetime

logger = logging.getLogger("veiloracle.insert_article")
supabase = get_supabase_client()

def log_system_event(event: str, status: str, details: Dict = None):
    """Inserts an operational log into the Supabase logs table."""
    if not supabase:
        logger.error(f"SUPABASE UNAVAILABLE | Log: {event} | {status} | {details}")
        return
    try:
        payload = {
            "event": event,
            "status": status,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        supabase.table("logs").insert(payload).execute()
    except Exception as e:
        logger.error(f"Failed to write to logs table: {e}")

def ensure_source_exists(source: str):
    """Ensure the news source exists in the sources table before linking."""
    if not supabase or not source:
        return
    try:
        # Upsert the source. (Uses predefined credibility_score default in SQL if new)
        supabase.table("sources").upsert({"name": source}, on_conflict="name").execute()
    except Exception as e:
        logger.warning(f"Failed to upsert source '{source}': {e}")

def insert_articles(articles: List[Dict[str, Any]]):
    """
    Inserts a batch of articles securely into Supabase PostgreSQL.
    Relies on SQL constraint `UNIQUE(title, source)` for deduplication, preventing
    UI duplicates and unnecessary DB updates.
    """
    if not supabase:
        logger.warning("Supabase client not initialized. Cannot insert articles.")
        return

    inserted_count = 0
    duplicate_count = 0

    for idx, article in enumerate(articles):
        source = article.get("source", "Unknown")
        title = article.get("title", "")
        
        # 1. Normalize Source
        ensure_source_exists(source)

        # 2. Build insertion payload matching SQL schema
        payload = {
            "title": title,
            "description": article.get("description", "")[:2000],  # Cap description limit
            "source": source,
            "location": article.get("location", "Unknown"),
            "region": article.get("region", "World").title(),
            "published_at": article.get("published_at", datetime.utcnow().isoformat()),
            "url": article.get("url", ""),
            "confidence": article.get("confidence", 0.0)
        }

        # 3. Insert into Supabase logic
        try:
            # Upsert will ignore conflict if the title and source are exactly the same
            # Since the unique key is (title, source)
            res = supabase.table("articles").upsert(
                payload, 
                on_conflict="title,source",
                ignore_duplicates=True  # Ensure real duplicates aren't processed.
            ).execute()
            
            if len(res.data) > 0:
                inserted_count += 1
            else:
                duplicate_count += 1

        except Exception as e:
            logger.error(f"DB Error while inserting article: {e}")
            log_system_event("ARTICLE_INSERT_FAILED", "ERROR", {"title": title, "error": str(e)})

    # Log operational status
    log_system_event(
        "PIPELINE_BATCH_INSERT", 
        "SUCCESS", 
        {"attempted": len(articles), "inserted": inserted_count, "duplicates": duplicate_count}
    )
    logger.info(f"Supabase Sync: inserted {inserted_count}, skipped {duplicate_count} duplicates.")

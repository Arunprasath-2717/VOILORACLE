"""
VEILORACLE — Real-time Subscription Listener
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Demonstrates backend-side listening for Supabase PostgreSQL changes.
Useful for triggering external notifications or derived side-effects.
"""

import logging
import asyncio
from backend.supabase_client import get_supabase_client

logger = logging.getLogger("veiloracle.realtime")
supabase = get_supabase_client()

def on_article_insert(payload):
    """Callback for all new articles inserted into the platform."""
    new_record = payload.get("record", {})
    logger.info(f"✨ REAL-TIME SIGNAL: New article from {new_record.get('source')} -> {new_record.get('title')[:60]}")

async def subscribe_to_live_intelligence():
    """
    Subscribes the backend to changes in the articles table.
    Enables true real-time reactive behavior on the server-side.
    """
    if not supabase:
        logger.warning("Supabase client not available for real-time subscription.")
        return

    logger.info("📡 Initializing Supabase Real-time Listener for 'articles'...")
    
    # Note: supabase-py's real-time support is handled via the 'realtime-py' subdependency
    # which uses websockets to listen to PostgreSQL 'REPLICA' changes.
    channel = supabase.channel("live_feed")
    channel.on(
        "postgres_changes",
        event="INSERT",
        schema="public",
        table="articles",
        callback=on_article_insert
    ).subscribe()
    
    logger.info("✓ Backend is now listening for incoming intelligence signals.")

if __name__ == "__main__":
    # Setup simple logging for standalone testing
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(subscribe_to_live_intelligence())
    loop.run_forever()

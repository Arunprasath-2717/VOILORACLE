"""
VEILORACLE — Message Queue Layer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Streaming architecture using Redis (or fallback to local queue via threading).
Redis is optional — if not installed or not running, uses an in-memory queue.
"""

import json
import logging
import queue

logger = logging.getLogger("veiloracle.queue")

_redis_client = None
_local_queue: queue.Queue = queue.Queue()

# Try to import and connect to Redis; if unavailable, fall back silently
try:
    import redis  # type: ignore
    from backend import config  # type: ignore
    _redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)
    _redis_client.ping()
    logger.info("Connected to Redis broker.")
except Exception as e:
    logger.warning("Redis not available (%s) — falling back to memory queue.", e)
    _redis_client = None


def push_articles(articles: list):
    """Push articles into the queue."""
    if not articles:
        return
    if _redis_client:
        try:
            for a in articles:
                _redis_client.lpush("veiloracle:news_pipeline", json.dumps(a))
            return
        except Exception as e:
            logger.error("Redis push failed: %s", e)

    # Fallback to in-memory queue
    for a in articles:
        _local_queue.put(a)


def pop_articles(batch_size: int = 100, timeout: int = 5) -> list:
    """Pop a batch of articles from the queue."""
    articles: list = []
    if _redis_client:
        try:
            for _ in range(batch_size):
                item = _redis_client.brpop("veiloracle:news_pipeline", timeout=1)
                if item:
                    articles.append(json.loads(item[1]))
                else:
                    break
            return articles
        except Exception as e:
            logger.error("Redis pop failed: %s", e)

    # Fallback to in-memory queue
    for _ in range(batch_size):
        try:
            articles.append(_local_queue.get_nowait())
        except queue.Empty:
            break

    return articles

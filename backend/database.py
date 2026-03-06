"""
VEILORACLE — Database Layer (SQLite + Upgraded Schema)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SQLite storage for articles, events, impacts, and pipeline runs.
Includes new fields: lifecycle, weight_score, fake_news, embedding (as JSON blob).
"""

import json
import logging
import sqlite3
from datetime import datetime

from backend import config  # type: ignore

logger = logging.getLogger("veiloracle.database")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(config.DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row[1] == column for row in rows)


def migrate_db(conn: sqlite3.Connection):
    migrations = [
        ("events", "importance_score", "ALTER TABLE events ADD COLUMN importance_score REAL DEFAULT 0.0"),
        ("events", "risk_score",       "ALTER TABLE events ADD COLUMN risk_score REAL DEFAULT 0.0"),
        ("events", "impact_json",      "ALTER TABLE events ADD COLUMN impact_json TEXT DEFAULT '[]'"),
        ("events", "lifecycle",        "ALTER TABLE events ADD COLUMN lifecycle TEXT DEFAULT 'emerging'"),
        ("events", "weight_score",     "ALTER TABLE events ADD COLUMN weight_score REAL DEFAULT 0.0"),
        ("articles", "url",            "ALTER TABLE articles ADD COLUMN url TEXT DEFAULT ''"),
        ("articles", "fake_news_label","ALTER TABLE articles ADD COLUMN fake_news_label TEXT DEFAULT 'Real'"),
        ("articles", "fake_news_score","ALTER TABLE articles ADD COLUMN fake_news_score REAL DEFAULT 1.0"),
        ("articles", "embedding_json", "ALTER TABLE articles ADD COLUMN embedding_json TEXT DEFAULT ''"),
    ]
    for table, col, sql in migrations:
        if not _column_exists(conn, table, col):
            try:
                conn.execute(sql)
                conn.commit()
                logger.info("Migration applied: added %s.%s", table, col)
            except Exception as e:
                logger.warning("Migration skipped (%s.%s): %s", table, col, e)


def init_db():
    conn = get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT DEFAULT '',
                source TEXT DEFAULT 'Unknown', url TEXT DEFAULT '', published_at TEXT,
                clean_text TEXT DEFAULT '', sentiment_label TEXT DEFAULT 'Neutral',
                sentiment_score REAL DEFAULT 0.0, impacts_json TEXT DEFAULT '[]',
                fake_news_label TEXT DEFAULT 'Real', fake_news_score REAL DEFAULT 1.0,
                embedding_json TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')), pipeline_run_id TEXT DEFAULT '');
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL, label TEXT NOT NULL,
                size INTEGER DEFAULT 1, is_cluster INTEGER DEFAULT 0,
                lifecycle TEXT DEFAULT 'emerging', weight_score REAL DEFAULT 0.0,
                sentiment_label TEXT DEFAULT 'Neutral', sentiment_score REAL DEFAULT 0.0,
                importance_score REAL DEFAULT 0.0, risk_score REAL DEFAULT 0.0,
                impact_json TEXT DEFAULT '[]',
                article_ids_json TEXT DEFAULT '[]', created_at TEXT DEFAULT (datetime('now')),
                pipeline_run_id TEXT DEFAULT '');
            CREATE TABLE IF NOT EXISTS impacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, article_id INTEGER, sector TEXT NOT NULL,
                direction TEXT NOT NULL, strength TEXT DEFAULT 'Neutral', confidence REAL DEFAULT 0.0,
                matched_keywords TEXT DEFAULT '', created_at TEXT DEFAULT (datetime('now')),
                pipeline_run_id TEXT DEFAULT '', FOREIGN KEY (article_id) REFERENCES articles(id));
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id TEXT PRIMARY KEY, started_at TEXT NOT NULL, finished_at TEXT,
                status TEXT DEFAULT 'running', article_count INTEGER DEFAULT 0,
                event_count INTEGER DEFAULT 0, error_message TEXT DEFAULT '');
            CREATE INDEX IF NOT EXISTS idx_articles_pipeline ON articles(pipeline_run_id);
            CREATE INDEX IF NOT EXISTS idx_events_pipeline ON events(pipeline_run_id);
            CREATE INDEX IF NOT EXISTS idx_impacts_sector ON impacts(sector);
            CREATE INDEX IF NOT EXISTS idx_articles_sentiment ON articles(sentiment_label);
        """)
        conn.commit()
        migrate_db(conn)
        logger.info("Database initialized: %s", config.DB_PATH)
    finally:
        conn.close()


def save_articles(articles: list, pipeline_run_id: str = "") -> list:
    conn = get_connection()
    ids: list = []
    try:
        for a in articles:
            s = a.get("sentiment", {})
            fn = a.get("fake_news_analysis", {})
            emb = a.get("embedding")
            emb_json = json.dumps(emb) if emb else ""
            cur = conn.execute(
                "INSERT INTO articles (title,description,source,url,published_at,clean_text,"
                "sentiment_label,sentiment_score,impacts_json,fake_news_label,fake_news_score,"
                "embedding_json,pipeline_run_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (a.get("title", ""), a.get("description", ""), a.get("source", "Unknown"),
                 a.get("url", ""), a.get("published_at", ""), a.get("clean_text", ""),
                 s.get("label", "Neutral"), float(s.get("compound", 0.0)),
                 json.dumps(a.get("impacts", [])),
                 fn.get("label", "Real"), float(fn.get("score", 1.0)),
                 emb_json, pipeline_run_id))
            ids.append(cur.lastrowid)
        conn.commit()
        logger.info("Saved %d articles.", len(ids))
    finally:
        conn.close()
    return ids


def save_events(events: list, article_db_ids: list, articles: list, pipeline_run_id: str = ""):
    conn = get_connection()
    try:
        for event in events:
            db_ids = [article_db_ids[i] for i in event.get("article_indices", []) if i < len(article_db_ids)]
            compounds = [articles[i].get("sentiment", {}).get("compound", 0.0)
                         for i in event.get("article_indices", []) if i < len(articles)]
            avg = sum(compounds) / len(compounds) if compounds else 0.0
            label = "Positive" if avg >= 0.05 else "Negative" if avg <= -0.05 else "Neutral"
            conn.execute(
                "INSERT INTO events (event_id,label,size,is_cluster,lifecycle,weight_score,"
                "sentiment_label,sentiment_score,importance_score,risk_score,impact_json,"
                "article_ids_json,pipeline_run_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (event["event_id"], event["label"], event["size"],
                 int(event.get("is_cluster", False)),
                 event.get("lifecycle", "emerging"),
                 float(event.get("weight_score", 0.0)),
                 label, round(float(avg), 4),  # type: ignore
                 float(event.get("importance_score", 0.0)),
                 float(event.get("risk_score", 0.0)),
                 json.dumps(event.get("impact_json", [])),
                 json.dumps(db_ids), pipeline_run_id))
        conn.commit()
        logger.info("Saved %d events.", len(events))
    finally:
        conn.close()


def save_impacts(articles: list, article_db_ids: list, pipeline_run_id: str = ""):
    conn = get_connection()
    count: int = 0
    try:
        for i, article in enumerate(articles):
            aid = article_db_ids[i] if i < len(article_db_ids) else None
            for imp in article.get("impacts", []):
                conn.execute(
                    "INSERT INTO impacts (article_id,sector,direction,strength,confidence,"
                    "matched_keywords,pipeline_run_id) VALUES (?,?,?,?,?,?,?)",
                    (aid, imp.get("sector", ""), imp.get("direction", ""),
                     imp.get("strength", "Neutral"), float(imp.get("confidence", 0.0)),
                     ", ".join(imp.get("matched_keywords", [])), pipeline_run_id))
                count += 1  # type: ignore
        conn.commit()
        logger.info("Saved %d impacts.", count)
    finally:
        conn.close()


def start_pipeline_run(run_id: str):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO pipeline_runs (id,started_at) VALUES (?,?)",
                     (run_id, datetime.utcnow().isoformat()))
        conn.commit()
    finally:
        conn.close()


def finish_pipeline_run(run_id: str, article_count: int, event_count: int,
                        status: str = "success", error: str = ""):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE pipeline_runs SET finished_at=?,status=?,article_count=?,event_count=?,"
            "error_message=? WHERE id=?",
            (datetime.utcnow().isoformat(), status, article_count, event_count, error, run_id))
        conn.commit()
    finally:
        conn.close()


# ── Query Helpers (Dashboard) ────────────────────────────────────────────────

def _rows_to_dicts(rows) -> list:
    return [dict(r) for r in rows]


def get_article_count() -> int:
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) as c FROM articles").fetchone()
        return row["c"] if row else 0
    except Exception as e:
        logger.error("get_article_count error: %s", e)
        return 0
    finally:
        conn.close()
    return 0


def get_recent_articles(limit: int = 50) -> list:
    conn = get_connection()
    try:
        return _rows_to_dicts(
            conn.execute("SELECT * FROM articles ORDER BY id DESC LIMIT ?", (limit,)).fetchall())
    except Exception as e:
        logger.error("get_recent_articles error: %s", e)
        return []
    finally:
        conn.close()
    return []


def get_all_events(limit: int = 100) -> list:
    conn = get_connection()
    try:
        return _rows_to_dicts(
            conn.execute("SELECT * FROM events ORDER BY importance_score DESC LIMIT ?",
                         (limit,)).fetchall())
    except Exception as e:
        logger.error("get_all_events error: %s", e)
        return []
    finally:
        conn.close()
    return []


def get_sentiment_distribution() -> dict:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT sentiment_label, count(*) as count FROM articles GROUP BY sentiment_label"
        ).fetchall()
        return {r["sentiment_label"]: r["count"] for r in rows}
    except Exception as e:
        logger.error("get_sentiment_distribution error: %s", e)
        return {"Positive": 0, "Negative": 0, "Neutral": 0}
    finally:
        conn.close()
    return {"Positive": 0, "Negative": 0, "Neutral": 0}


def get_sector_impact_summary() -> list:
    conn = get_connection()
    try:
        return _rows_to_dicts(conn.execute("""
            SELECT sector, count(*) as total,
                   sum(CASE WHEN direction='Positive' THEN 1 ELSE 0 END) as pos,
                   sum(CASE WHEN direction='Negative' THEN 1 ELSE 0 END) as neg
            FROM impacts GROUP BY sector ORDER BY total DESC LIMIT 30
        """).fetchall())
    except Exception as e:
        logger.error("get_sector_impact_summary error: %s", e)
        return []
    finally:
        conn.close()
    return []


def get_recent_pipeline_runs(limit: int = 10) -> list:
    conn = get_connection()
    try:
        return _rows_to_dicts(
            conn.execute("SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT ?",
                         (limit,)).fetchall())
    except Exception as e:
        logger.error("get_recent_pipeline_runs error: %s", e)
        return []
    finally:
        conn.close()
    return []


def get_articles_by_ids(article_ids: list) -> list:
    if not article_ids:
        return []
    conn = get_connection()
    try:
        placeholders = ",".join("?" for _ in article_ids)
        return _rows_to_dicts(
            conn.execute(f"SELECT * FROM articles WHERE id IN ({placeholders})",
                         article_ids).fetchall())
    except Exception as e:
        logger.error("get_articles_by_ids error: %s", e)
        return []
    finally:
        conn.close()
    return []

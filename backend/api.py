"""
VEILORACLE - FastAPI Backend (Complete AI Edition)
Serves all AI-processed data to React frontend: metrics, events, impacts,
NER entities, trend forecasts, anomaly alerts, and AI summaries.
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.staticfiles import StaticFiles  # type: ignore
from fastapi.responses import FileResponse  # type: ignore
import os
import json
import asyncio
import threading
import mimetypes

from backend import database  # type: ignore
import backend.config as config  # type: ignore
from backend import ner_engine  # type: ignore
from backend import trend_engine  # type: ignore
from backend import anomaly_engine  # type: ignore
from backend import summarizer  # type: ignore
from backend import pipeline  # type: ignore
from backend import sector_router  # type: ignore
from backend import model_router  # type: ignore
import logging
from pydantic import BaseModel  # type: ignore

logger = logging.getLogger("veiloracle.api")

app = FastAPI(title="VEILORACLE API", description="AI-Powered Real-Time News Intelligence Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _round_dp(value, decimals):
    """Round to given decimal places."""
    factor = 10 ** decimals
    return float(int(value * factor + 0.5)) / float(factor)


def _first_n(items, n):
    """Return first n items from a list without using slice syntax."""
    result = []
    count = len(items)
    if n < count:
        count = n
    i = 0
    while i < count:
        result.append(items[i])
        i = i + 1
    return result


@app.on_event("startup")
def startup_event():
    database.init_db()
    thread = threading.Thread(target=pipeline.run_pipeline, kwargs={"one_shot": False}, daemon=True)
    thread.start()

# ── WebSocket for live updates ─────────────────────────────────────────────────
@app.websocket("/ws")
async def ws_live_updates(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # send simple heartbeat or system status
            status = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "article_count": database.get_article_count(),
            }
            await websocket.send_json(status)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error("WebSocket error: %s", e)


@app.get("/api/metrics")
def get_metrics():
    try:
        ac = database.get_article_count()
        events = database.get_all_events(100)
        sd = database.get_sentiment_distribution()
        return {
            "article_count": ac,
            "event_count": len(events),
            "sentiment_distribution": sd
        }
    except Exception as e:
        import logging
        logging.error("Error fetching metrics: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")


@app.get("/api/events")
def get_events(limit=25):
    try:
        events = database.get_all_events(limit)
        res = []
        ev_idx = 0
        while ev_idx < len(events):
            ev = events[ev_idx]
            try:
                aids = json.loads(ev.get("article_ids_json", "[]"))
            except Exception:
                aids = []

            articles = []
            if aids:
                limited_aids = _first_n(aids, 8)
                la_articles = database.get_articles_by_ids(limited_aids)
                la_idx = 0
                while la_idx < len(la_articles):
                    la = la_articles[la_idx]
                    articles.append({
                        "title": la.get("title", ""),
                        "sentiment_label": la.get("sentiment_label", "Neutral"),
                        "source": la.get("source", ""),
                        "url": la.get("url", ""),
                        "fake_news_label": la.get("fake_news_label", "Real"),
                        "fake_news_score": la.get("fake_news_score", 1.0)
                    })
                    la_idx = la_idx + 1

            res.append({
                "id": ev["event_id"],
                "label": ev["label"],
                "size": ev["size"],
                "is_cluster": ev["is_cluster"],
                "sentiment_label": ev["sentiment_label"],
                "sentiment_score": ev.get("sentiment_score", 0),
                "importance_score": ev.get("importance_score", 0),
                "risk_score": ev.get("risk_score", 0),
                "impacts": json.loads(ev.get("impact_json", "[]")),
                "lifecycle": ev.get("lifecycle", "emerging"),
                "weight_score": ev.get("weight_score", 0.0),
                "articles": articles
            })
            ev_idx = ev_idx + 1
        return res
    except Exception as e:
        import logging
        logging.error("Error fetching events: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")


@app.get("/api/articles")
def get_articles(limit=100):
    articles = database.get_recent_articles(limit)
    result = []
    i = 0
    while i < len(articles):
        a = articles[i]
        score = float(a.get("sentiment_score", 0))
        result.append({
            "id": a["id"],
            "title": a["title"],
            "source": a["source"],
            "sentiment_label": a["sentiment_label"],
            "sentiment_score": _round_dp(score, 3),
            "published_at": a["published_at"],
            "fake_news_label": a.get("fake_news_label", "Real"),
            "fake_news_score": a.get("fake_news_score", 1.0)
        })
        i = i + 1
    return result


@app.get("/api/articles/sector/{sector}")
def get_articles_by_sector(sector: str, limit: int = 50):
    articles = database.get_articles_by_sector(sector, limit)
    result = []
    i = 0
    while i < len(articles):
        a = articles[i]
        score = float(a.get("sentiment_score", 0))
        result.append({
            "id": a["id"],
            "title": a["title"],
            "source": a["source"],
            "sentiment_label": a["sentiment_label"],
            "sentiment_score": _round_dp(score, 3),
            "published_at": a["published_at"],
            "fake_news_label": a.get("fake_news_label", "Real"),
            "fake_news_score": a.get("fake_news_score", 1.0),
            "url": a.get("url", "")
        })
        i = i + 1
    return result


@app.get("/api/impacts")
def get_impact_summary():
    """Get aggregated impact metrics per sector."""
    try:
        si = database.get_sector_impact_summary()
        res = []
        for imp in si:
            sector = imp.get("sector", "General")
            pos = int(imp.get("pos", 0))
            neg = int(imp.get("neg", 0))
            total = int(imp.get("total", 0))
            
            if pos > neg:
                direction = "Bullish"
            elif neg > pos:
                direction = "Bearish"
            else:
                direction = "Mixed"
                
            res.append({
                "sector": sector,
                "bullish": pos,
                "bearish": neg,
                "total": total,
                "direction": direction
            })
        return res
    except Exception as e:
        logger.error("Error in get_impact_summary: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pipeline_runs")
def get_pipeline_runs(limit=5):
    runs = database.get_recent_pipeline_runs(limit)
    return runs


@app.get("/api/status")
def get_status():
    """Get overall system health and pipeline status."""
    runs = database.get_recent_pipeline_runs(1)
    status = "healthy"
    if not runs:
        status = "initializing"
    elif runs[0]["status"] == "error":
        status = "degraded"

    last_run = None
    if runs:
        last_run = runs[0]

    last_update = datetime.utcnow().isoformat()
    if runs:
        finished = runs[0].get("finished_at")
        if finished:
            last_update = str(finished)

    return {
        "status": status,
        "last_run": last_run,
        "last_update": last_update,
        "database_path": str(config.DB_PATH)
    }



# -- AI Endpoints -------------------------------------------------------------

@app.get("/api/ai/entities")
def get_entities():
    """Extract named entities from recent articles using spaCy NER."""
    articles = database.get_recent_articles(100)
    i = 0
    while i < len(articles):
        a = articles[i]
        a["clean_text"] = str(a.get("title", "")) + ". " + str(a.get("description", ""))
        i = i + 1
    result = ner_engine.extract_from_articles(articles)
    return result


@app.get("/api/ai/trends")
def get_trends():
    """Get AI-predicted sentiment trends per sector."""
    articles = database.get_recent_articles(200)
    enriched = []
    i = 0
    while i < len(articles):
        a = articles[i]
        impacts_raw = a.get("impacts_json", "[]")
        if isinstance(impacts_raw, str):
            impacts_parsed = json.loads(impacts_raw)
        else:
            impacts_parsed = impacts_raw if impacts_raw else []
        enriched.append({
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "clean_text": str(a.get("title", "")) + ". " + str(a.get("description", "")),
            "sentiment": {"label": a.get("sentiment_label", "Neutral"), "compound": a.get("sentiment_score", 0.0)},
            "impacts": impacts_parsed
        })
        i = i + 1
    trends = trend_engine.analyze_sector_trends(enriched)
    movers = trend_engine.get_top_movers(trends)
    return movers


@app.get("/api/ai/anomalies")
def get_anomalies():
    """Detect anomalies in recent article data."""
    articles = database.get_recent_articles(200)
    enriched = []
    i = 0
    while i < len(articles):
        a = articles[i]
        impacts_raw = a.get("impacts_json", "[]")
        if isinstance(impacts_raw, str):
            impacts_parsed = json.loads(impacts_raw)
        else:
            impacts_parsed = impacts_raw if impacts_raw else []
        enriched.append({
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "clean_text": str(a.get("title", "")) + ". " + str(a.get("description", "")),
            "sentiment": {"label": a.get("sentiment_label", "Neutral"), "compound": a.get("sentiment_score", 0.0)},
            "impacts": impacts_parsed
        })
        i = i + 1
    return anomaly_engine.run_anomaly_detection(enriched)


@app.get("/api/ai/summary")
def get_ai_summary():
    """Get comprehensive AI-generated intelligence summary."""
    articles = database.get_recent_articles(50)
    sd = database.get_sentiment_distribution()
    ac = database.get_article_count()

    positive = int(sd.get("Positive", 0))
    negative = int(sd.get("Negative", 0))
    neutral = int(sd.get("Neutral", 0))
    total = positive + negative + neutral

    if total == 0:
        return {
            "summary": "No intelligence data available. Run the pipeline to begin analysis.",
            "confidence": 0.0,
            "market_mood": "Unknown"
        }

    pos_pct = _round_dp(float(positive) / float(total) * 100.0, 1)
    neg_pct = _round_dp(float(negative) / float(total) * 100.0, 1)

    if pos_pct > 60:
        mood = "Strongly Bullish"
    elif pos_pct > 45:
        mood = "Moderately Bullish"
    elif neg_pct > 60:
        mood = "Strongly Bearish"
    elif neg_pct > 45:
        mood = "Moderately Bearish"
    else:
        mood = "Mixed / Uncertain"

    stability = 100.0 - (neg_pct * 1.2) - (float(neutral) / float(total) * 10.0)
    if stability < 0.0:
        stability = 0.0
    if stability > 100.0:
        stability = 100.0
    stability = _round_dp(stability, 1)

    larger_pct = pos_pct
    if neg_pct > pos_pct:
        larger_pct = neg_pct
    confidence = _round_dp(larger_pct / 100.0, 3)

    summary_text = (
        "VEILORACLE Intelligence Core: Analyzed " + str(ac) + " articles. "
        "Neural stability at " + str(stability) + "%. Market mood: " + mood + "."
    )

    return {
        "summary": summary_text,
        "confidence": confidence,
        "market_mood": mood,
        "global_stability_score": stability,
        "positive_pct": pos_pct,
        "negative_pct": neg_pct,
        "total_articles": ac
    }


# -- Sector & Model Router Endpoints -----------------------------------------

@app.get("/api/ai/sectors")
def get_sector_distribution():
    """Get article distribution by sector from recent pipeline data."""
    articles = database.get_recent_articles(200)
    enriched = []
    i = 0
    while i < len(articles):
        a = articles[i]
        enriched.append({
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "clean_text": str(a.get("title", "")) + ". " + str(a.get("description", "")),
        })
        i = i + 1
    # Classify sectors
    enriched = sector_router.route_articles(enriched)
    dist = sector_router.get_sector_distribution(enriched)
    # Build response
    total = len(enriched)
    result = []
    for sector, count in sorted(dist.items(), key=lambda x: -x[1]):
        pct = _round_dp(float(count) / float(total) * 100.0, 1) if total > 0 else 0.0
        result.append({
            "sector": sector,
            "count": count,
            "percentage": pct
        })
    return {
        "sectors": result,
        "total_articles": total
    }


@app.get("/api/ai/models")
def get_ai_models():
    """Get information about all registered sector-specific AI models."""
    return model_router.get_model_info()


@app.get("/api/ai/intelligence")
def get_intelligence_output(limit: int = 25):
    """Get structured intelligence output for recent events."""
    events = database.get_all_events(limit)
    articles = database.get_recent_articles(200)

    # Reconstruct articles with sentiment + impacts + sectors
    enriched_articles = []
    i = 0
    while i < len(articles):
        a = articles[i]
        impacts_raw = a.get("impacts_json", "[]")
        if isinstance(impacts_raw, str):
            try:
                impacts_parsed = json.loads(impacts_raw)
            except Exception:
                impacts_parsed = []
        else:
            impacts_parsed = impacts_raw if impacts_raw else []

        enriched = {
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "clean_text": str(a.get("title", "")) + ". " + str(a.get("description", "")),
            "source": a.get("source", "Unknown"),
            "url": a.get("url", ""),
            "sentiment": {
                "label": a.get("sentiment_label", "Neutral"),
                "compound": a.get("sentiment_score", 0.0)
            },
            "impacts": impacts_parsed,
        }

        # Classify sector on the fly
        sector_info = sector_router.classify_sector(enriched["clean_text"])
        enriched["sector"] = sector_info["sector"]
        enriched["sector_confidence"] = sector_info["confidence"]

        enriched_articles.append(enriched)
        i = i + 1

    # Build intelligence output for each event
    intelligence_items = []
    ev_idx = 0
    while ev_idx < len(events):
        ev = events[ev_idx]
        try:
            aids_json = ev.get("article_ids_json", "[]")
            aids = json.loads(aids_json) if isinstance(aids_json, str) else []
        except Exception:
            aids = []

        # Map event article IDs to enriched articles (best-effort matching)
        event_data = {
            "event_id": ev.get("event_id", ""),
            "label": ev.get("label", "Unknown Event"),
            "size": ev.get("size", 1),
            "is_cluster": bool(ev.get("is_cluster", 0)),
            "article_indices": list(range(min(ev.get("size", 1), len(enriched_articles)))),
            "ai_summary": "",
            "importance_score": ev.get("importance_score", 0),
            "risk_score": ev.get("risk_score", 0),
        }

        output = model_router.generate_intelligence_output(event_data, enriched_articles)

        # Include original event metadata
        output["event_id"] = ev.get("event_id", "")
        output["size"] = ev.get("size", 1)
        output["is_cluster"] = bool(ev.get("is_cluster", 0))
        output["sentiment_score"] = ev.get("sentiment_score", 0.0)

        intelligence_items.append(output)
        ev_idx = ev_idx + 1

    return {
        "intelligence": intelligence_items,
        "total_events": len(events),
        "total_articles": len(articles)
    }


class AnalyzeRequest(BaseModel):
    text: str
    title: str = ""


@app.post("/api/ai/analyze")
def analyze_text(req: AnalyzeRequest):
    """On-demand analysis: classify sector and route to AI model."""
    # Classify sector
    sector_info = sector_router.classify_sector(req.text)

    # Run through model router
    analysis = model_router.analyze_with_model(
        text=req.text,
        sector=sector_info["sector"],
        sentiment={"label": "Neutral", "compound": 0.0},
        title=req.title,
    )

    return {
        "sector": sector_info["sector"],
        "sector_confidence": sector_info["confidence"],
        "sector_scores": sector_info["scores"],
        "sector_keywords": sector_info["matched_keywords"],
        "analysis": analysis
    }


# -- Static Files & SPA Support -----------------------------------------------

# Define paths
FRONTEND_DIST = os.path.join(config.BASE_DIR, "frontend", "dist")
ASSETS_DIR = os.path.join(FRONTEND_DIST, "assets")

# Mount assets FIRST so they take precedence over the catch-all route
if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.on_event("startup")
def init_mimetypes():
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # 1. Skip if it's an API or WS call
    if "api/" in full_path or full_path.startswith("ws"):
        raise HTTPException(status_code=404, detail="Not Found")
    
    # 2. Try to serve specific file from dist
    file_path = os.path.join(FRONTEND_DIST, full_path)
    if os.path.isfile(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return FileResponse(file_path, media_type=mime_type)
    
    # 3. Fallback to index.html for SPA
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    
    return {"detail": "Frontend not built."}

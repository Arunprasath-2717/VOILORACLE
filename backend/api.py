"""
VEILORACLE - FastAPI Backend (Complete AI Edition)
Serves all AI-processed data to React frontend: metrics, events, impacts,
NER entities, trend forecasts, anomaly alerts, and AI summaries.
"""

from datetime import datetime

from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
import json

from backend import database  # type: ignore
import backend.config as config  # type: ignore
from backend import ner_engine  # type: ignore
from backend import trend_engine  # type: ignore
from backend import anomaly_engine  # type: ignore
from backend import summarizer  # type: ignore
from backend import pipeline  # type: ignore
from backend import gemini_engine  # type: ignore
import threading
from pydantic import BaseModel  # type: ignore

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


# -- Core Endpoints -----------------------------------------------------------

@app.get("/api/metrics")
def get_metrics():
    ac = database.get_article_count()
    events = database.get_all_events(100)
    sd = database.get_sentiment_distribution()
    return {
        "article_count": ac,
        "event_count": len(events),
        "sentiment_distribution": sd
    }


@app.get("/api/events")
def get_events(limit=25):
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
                    "url": la.get("url", "")
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
            "articles": articles
        })
        ev_idx = ev_idx + 1
    return res


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
            "published_at": a["published_at"]
        })
        i = i + 1
    return result


@app.get("/api/impacts")
def get_impact_summary():
    si = database.get_sector_impact_summary()
    sa = {}
    if si:
        idx = 0
        while idx < len(si):
            imp = si[idx]
            s = imp["sector"]
            if s not in sa:
                sa[s] = {"bullish": 0, "bearish": 0, "total": 0}
            entry = sa[s]
            direction_str = str(imp["direction"])
            if "Bullish" in direction_str:
                entry["bullish"] = entry["bullish"] + imp["count"]
            elif "Bearish" in direction_str:
                entry["bearish"] = entry["bearish"] + imp["count"]
            entry["total"] = entry["total"] + imp["count"]
            idx = idx + 1

    res = []
    sorted_sectors = sorted(sa.keys(), key=lambda x: -int(sa[x]["total"]))
    for s in sorted_sectors:
        d = sa[s]
        if d["bullish"] > d["bearish"]:
            direction = "Bullish"
        elif d["bearish"] > d["bullish"]:
            direction = "Bearish"
        else:
            direction = "Mixed"
        res.append({
            "sector": s,
            "bullish": d["bullish"],
            "bearish": d["bearish"],
            "total": d["total"],
            "direction": direction
        })
    return res


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


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.post("/api/ai/chat")
def chat_with_oracle(req: ChatRequest):
    """Chat with the VOILORACLE Intelligence Core using Gemini."""
    system_instruction = (
        "You are the VOILORACLE Intelligence Core, a state-of-the-art AI monitoring global signals. "
        "You are professional, analytical, and sharp. Use the data provided in the user's query if available. "
        "Keep responses concise and impactful."
    )

    context = ""
    if "sentiment" in req.message.lower() or "market" in req.message.lower():
        sd = database.get_sentiment_distribution()
        context = "\nCurrent Global Sentiment Distribution: " + json.dumps(sd)

    prompt = req.message + context
    response = gemini_engine.generate_response(prompt, system_instruction)
    return {"response": response}


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

"""
Kronaxis — Event Ranker (Explainable Importance Scoring)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ranks events (article clusters) by composite importance score.
Score = f(article_count, sentiment_intensity, source_credibility)

Each component is normalized to [0, 1] before weighting, so the final
score is interpretable as a 0–100 scale.
"""

import logging
import json
import math
from typing import List, Dict, Any

from backend import config  # type: ignore

logger = logging.getLogger("Kronaxis.event_ranker")


# ── Weights (empirically balanced — can be tuned) ─────────────────────────
W_COVERAGE = 0.40      # How many articles cover this event
W_SENTIMENT = 0.30     # Emotional intensity (strong = important)
W_CREDIBILITY = 0.30   # Are trusted sources reporting this?
W_TOTAL = W_COVERAGE + W_SENTIMENT + W_CREDIBILITY


def _round_1dp(val: Any) -> float:
    """Helper to round to 1 decimal place safely."""
    try:
        return float(f"{float(val):.1f}")
    except (ValueError, TypeError):
        return 0.0


def _get_source_credibility(source: str) -> float:
    """Lookup source credibility from config, default if unknown."""
    if not source:
        return config.DEFAULT_CREDIBILITY
    source_lower = source.lower()
    for key, val in config.SOURCE_CREDIBILITY.items():
        if key.lower() in source_lower:
            return val
    return config.DEFAULT_CREDIBILITY


def _generate_why_it_matters(
    size: int,
    sentiment_intensity: float,
    credibility_avg: float,
    sentiment_label: str,
    trusted_sources: List[str],
) -> List[str]:
    """
    Generate human-readable reasons for why an event is important.
    """
    reasons = []

    # Coverage-based
    if size >= 10:
        reasons.append(f"High global coverage ({size} sources reporting)")
    elif size >= 5:
        reasons.append(f"Significant media attention ({size} sources)")
    elif size >= 3:
        reasons.append(f"Multi-source confirmation ({size} sources)")

    # Sentiment-based
    if sentiment_intensity > 0.85:
        if sentiment_label == "Negative":
            reasons.append("Strong negative sentiment detected — may indicate elevated risk")
        elif sentiment_label == "Positive":
            reasons.append("Strong positive momentum across coverage")
        else:
            reasons.append("High emotional intensity across sources")
    elif sentiment_intensity > 0.6:
        reasons.append("Notable emotional resonance in reporting")

    # Credibility-based
    if credibility_avg > 0.85:
        top_trusted = [ts for i, ts in enumerate(trusted_sources) if i < 3]
        reasons.append(f"Verified by trusted sources ({', '.join(top_trusted)})")
    elif credibility_avg > 0.6:
        reasons.append("Reported by moderately credible sources")

    if not reasons:
        reasons.append("Emerging signal — monitoring recommended")

    return reasons


def compute_confidence_score(source: str, cluster_size: int = 1) -> dict:
    """
    Compute a evidence-based confidence score for an article.
    """
    source_cred = _get_source_credibility(source)
    agreement_score = min(cluster_size / 5.0, 1.0)
    raw = source_cred * 0.7 + agreement_score * 0.3
    confidence_pct = _round_1dp(min(raw * 100, 100.0))

    if confidence_pct >= 80:
        level = "High"
    elif confidence_pct >= 55:
        level = "Moderate"
    else:
        level = "Low"

    return {
        "score": confidence_pct,
        "level": level,
        "source_trust": _round_1dp(source_cred * 100),
        "agreement_score": _round_1dp(agreement_score * 100),
    }


def compute_event_score(event: Dict[str, Any], articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute a ranked importance score for a single event/cluster.
    """
    size = int(event.get("size", 1))
    coverage_raw = math.log2(size + 1)
    coverage_norm = min(coverage_raw / 5.0, 1.0)

    sentiment_map = {"Positive": 1.0, "Negative": 1.0, "Neutral": 0.3}

    try:
        article_ids_raw = event.get("article_ids_json", "[]")
        if isinstance(article_ids_raw, str):
            article_ids = json.loads(article_ids_raw)
        else:
            article_ids = article_ids_raw if article_ids_raw else []
    except Exception:
        article_ids = []

    article_map = {a.get("id"): a for a in articles if a.get("id")}
    cluster_articles = [article_map[aid] for aid in article_ids if aid in article_map]

    if cluster_articles:
        sentiments = [
            sentiment_map.get(a.get("sentiment_label", "Neutral"), 0.3)
            for a in cluster_articles
        ]
        sentiment_intensity = sum(sentiments) / len(sentiments)
    else:
        event_sentiment = event.get("sentiment_label", "Neutral")
        sentiment_intensity = sentiment_map.get(event_sentiment, 0.3)

    trusted_sources = []
    if cluster_articles:
        creds = []
        for a in cluster_articles:
            src = a.get("source", "")
            c = _get_source_credibility(src)
            creds.append(c)
            if c >= 0.8 and src and src not in trusted_sources:
                trusted_sources.append(src)
        credibility_avg = sum(creds) / len(creds)
    else:
        credibility_avg = config.DEFAULT_CREDIBILITY

    raw_score = (
        coverage_norm * W_COVERAGE +
        sentiment_intensity * W_SENTIMENT +
        credibility_avg * W_CREDIBILITY
    )
    final_score = _round_1dp(min(raw_score * 100, 100.0))

    sentiment_label = event.get("sentiment_label", "Neutral")
    why = _generate_why_it_matters(
        size, sentiment_intensity, credibility_avg,
        sentiment_label, trusted_sources,
    )

    return {
        "event_id": event.get("event_id", ""),
        "label": event.get("label", "Unknown Event"),
        "size": size,
        "sentiment_label": sentiment_label,
        "ranked_score": final_score,
        "why_it_matters": why,
        "articles": [
            {
                "title": a.get("title", ""),
                "source": a.get("source", ""),
                "sentiment_label": a.get("sentiment_label", "Neutral"),
                "url": a.get("url", ""),
            }
            for i, a in enumerate(cluster_articles) if i < 5
        ],
    }


def rank_top_events(
    events: List[Dict[str, Any]],
    articles: List[Dict[str, Any]],
    top_n: int = 5,
) -> List[Dict[str, Any]]:
    """
    Score and rank all events, return the top N.
    """
    scored = []
    for ev in events:
        try:
            scored_event = compute_event_score(ev, articles)
            scored.append(scored_event)
        except Exception as e:
            logger.warning("Failed to score event: %s", e)

    scored.sort(key=lambda x: -x["ranked_score"])
    
    result = []
    count = min(top_n, len(scored))
    for i in range(count):
        result.append(scored[i])
    
    return result

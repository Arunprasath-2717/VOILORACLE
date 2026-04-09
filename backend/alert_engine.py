"""
Kronaxis — Proactive Alert Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monitors the live intelligence database for critical events.
Uses multi-source consensus: an event must be confirmed by 2+
independent sources to be flagged as a true alert.
"""

import logging
import re
import time
from datetime import datetime, timedelta
from collections import defaultdict

from backend import database

logger = logging.getLogger("Kronaxis.alerts")

# ── Threat Keywords ──────────────────────────────────────────
CRITICAL_KEYWORDS = [
    "war", "attack", "nuclear", "invasion", "bombing", "terrorism",
    "crisis", "emergency", "catastrophe", "assassination", "coup",
    "pandemic", "outbreak", "collapse"
]
HIGH_KEYWORDS = [
    "conflict", "sanctions", "missile", "threat", "breach", "escalat",
    "crash", "surge", "collapse", "hack", "ransomware", "cyber attack",
    "explosion", "hostage", "martial law"
]
MEDIUM_KEYWORDS = [
    "tension", "dispute", "concern", "warning", "risk", "alert",
    "volatile", "instability", "protest", "shutdown", "disruption"
]

# Cache to avoid duplicate alert spam
_alert_cache = {"data": None, "timestamp": 0, "ttl": 120}


def _classify_severity(text: str) -> tuple:
    """Returns (severity, matched_keywords)."""
    text_lower = text.lower()
    matched = []

    for kw in CRITICAL_KEYWORDS:
        if kw in text_lower:
            matched.append(kw)
    if matched:
        return "Critical", matched

    for kw in HIGH_KEYWORDS:
        if kw in text_lower:
            matched.append(kw)
    if matched:
        return "High", matched

    for kw in MEDIUM_KEYWORDS:
        if kw in text_lower:
            matched.append(kw)
    if matched:
        return "Medium", matched

    return "Low", []


def _find_consensus_clusters(articles: list) -> list:
    """
    Group articles by normalized topic. An alert is only valid if 2+
    independent sources report on the same topic (multi-source consensus).
    """
    topic_groups = defaultdict(list)

    for a in articles:
        title = str(a.get("title", "")).strip()
        if len(title) < 10:
            continue

        # Normalize: extract key noun phrases for grouping
        words = re.findall(r'\b[a-z]{4,}\b', title.lower())
        if len(words) < 2:
            continue

        # Use the first 3 significant words as a fingerprint
        key = " ".join(sorted(words[:5]))
        topic_groups[key].append(a)

    # Filter: only keep clusters with 2+ unique sources
    validated = []
    for key, group in topic_groups.items():
        sources = set(a.get("source", "Unknown") for a in group)
        if len(sources) >= 2:
            validated.append({
                "key": key,
                "articles": group,
                "sources": list(sources),
                "source_count": len(sources),
            })

    return validated


def generate_alerts(hours_back: int = 6, max_alerts: int = 20) -> list:
    """
    Scan the database for recent articles and generate validated alerts.
    Only events confirmed by multiple independent sources are promoted.
    """
    now = time.time()
    if _alert_cache["data"] and (now - _alert_cache["timestamp"]) < _alert_cache["ttl"]:
        return _alert_cache["data"]

    try:
        all_articles = database.get_recent_articles(500)
    except Exception as e:
        logger.error("Failed to fetch articles for alerts: %s", e)
        return []

    # Filter to recent articles
    cutoff = datetime.utcnow() - timedelta(hours=hours_back)
    recent = []
    for a in all_articles:
        pub = a.get("published_at", "")
        try:
            if pub:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00").replace("+00:00", ""))
                if dt >= cutoff:
                    recent.append(a)
            else:
                recent.append(a)  # If no date, include it
        except Exception:
            recent.append(a)

    if not recent:
        recent = all_articles[:100]  # Fallback: use latest 100

    # Find multi-source consensus clusters
    clusters = _find_consensus_clusters(recent)

    alerts = []
    for cluster in clusters:
        # Use the first article's title as the alert headline
        lead = cluster["articles"][0]
        title = lead.get("title", "Unknown Event")
        combined_text = " ".join(
            str(a.get("title", "")) + " " + str(a.get("description", ""))
            for a in cluster["articles"]
        )

        severity, keywords = _classify_severity(combined_text)

        # Compute aggregate sentiment
        sentiments = [a.get("sentiment_label", "Neutral") for a in cluster["articles"]]
        neg_count = sentiments.count("Negative")
        pos_count = sentiments.count("Positive")

        if neg_count > pos_count:
            sentiment = "Negative"
        elif pos_count > neg_count:
            sentiment = "Positive"
        else:
            sentiment = "Mixed"

        alerts.append({
            "id": f"alert_{hash(title) % 100000:05d}",
            "title": title,
            "severity": severity,
            "sentiment": sentiment,
            "source_count": cluster["source_count"],
            "sources": cluster["sources"][:5],
            "article_count": len(cluster["articles"]),
            "keywords": keywords[:5],
            "timestamp": lead.get("published_at", datetime.utcnow().isoformat() + "Z"),
            "description": str(lead.get("description", ""))[:300],
        })

    # Sort by severity priority
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    alerts.sort(key=lambda a: (severity_order.get(a["severity"], 4), -a["source_count"]))

    result = alerts[:max_alerts]

    _alert_cache["data"] = result
    _alert_cache["timestamp"] = now

    return result

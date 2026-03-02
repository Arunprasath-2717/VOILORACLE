"""
VEILORACLE — Anomaly Detection Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uses statistical z-score analysis to detect unusual spikes in:
  - Article volume per sector
  - Sudden sentiment shifts
  - Abnormal keyword frequency
"""

import logging
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime

logger = logging.getLogger("veiloracle.anomaly")

# Z-score threshold for flagging anomalies
Z_THRESHOLD = 2.0


def z_score_detect(values: list[float], threshold: float = Z_THRESHOLD) -> list[dict]:
    """Detect anomalies in a list of values using z-score method."""
    if len(values) < 3:
        return []

    arr = np.array(values, dtype=float)
    mean = arr.mean()
    std = arr.std()

    if std == 0:
        return []

    z_scores = (arr - mean) / std
    anomalies = []
    for i, (val, z) in enumerate(zip(values, z_scores)):
        if abs(z) >= threshold:
            anomalies.append({
                "index": i,
                "value": round(float(val), 4),
                "z_score": round(float(z), 4),
                "type": "spike" if z > 0 else "drop",
                "severity": "critical" if abs(z) >= 3.0 else "warning"
            })

    return anomalies


def detect_volume_anomalies(articles: list[dict]) -> list[dict]:
    """Detect anomalous article volume per sector."""
    sector_counts = Counter()
    for article in articles:
        for impact in article.get("impacts", []):
            sector_counts[impact["sector"]] += 1

    if not sector_counts:
        return []

    counts = list(sector_counts.values())
    names = list(sector_counts.keys())

    anomalies = z_score_detect(counts)
    results = []
    for a in anomalies:
        sector = names[a["index"]]
        results.append({
            "sector": sector,
            "metric": "article_volume",
            "count": int(a["value"]),
            "z_score": a["z_score"],
            "type": a["type"],
            "severity": a["severity"],
            "message": f"{'Unusual surge' if a['type'] == 'spike' else 'Unusual drop'} in {sector} coverage ({int(a['value'])} articles, z={a['z_score']:.1f})"
        })

    return results


def detect_sentiment_anomalies(articles: list[dict]) -> list[dict]:
    """Detect articles with extreme sentiment scores."""
    if not articles:
        return []

    sentiments = [a.get("sentiment", {}).get("compound", 0.0) for a in articles]
    anomalies = z_score_detect(sentiments, threshold=2.5)

    results = []
    for a in anomalies:
        article = articles[a["index"]]
        results.append({
            "article_title": article.get("title", "Unknown"),
            "metric": "sentiment_extreme",
            "sentiment_score": a["value"],
            "z_score": a["z_score"],
            "type": "extremely_positive" if a["type"] == "spike" else "extremely_negative",
            "severity": a["severity"],
            "message": f"Extreme {'positive' if a['type'] == 'spike' else 'negative'} sentiment detected: \"{article.get('title', '')[:60]}...\" (score={a['value']:.2f})"
        })

    return results


def detect_sector_shift_anomalies(articles: list[dict]) -> list[dict]:
    """Detect sectors with unusual sentiment direction shifts."""
    sector_sentiments = defaultdict(list)

    for article in articles:
        score = article.get("sentiment", {}).get("compound", 0.0)
        for impact in article.get("impacts", []):
            sector_sentiments[impact["sector"]].append(score)

    results = []
    for sector, scores in sector_sentiments.items():
        if len(scores) < 3:
            continue

        # Check for sudden reversals
        avg = sum(scores) / len(scores)
        recent = scores[-3:]
        recent_avg = sum(recent) / len(recent)
        shift = recent_avg - avg

        if abs(shift) > 0.3:  # Significant shift
            results.append({
                "sector": sector,
                "metric": "sentiment_shift",
                "shift_magnitude": round(float(shift), 4),
                "type": "bullish_reversal" if shift > 0 else "bearish_reversal",
                "severity": "critical" if abs(shift) > 0.5 else "warning",
                "message": f"{'Bullish' if shift > 0 else 'Bearish'} reversal in {sector} (shift={shift:+.2f})"
            })

    return results


def run_anomaly_detection(articles: list[dict]) -> dict:
    """Run all anomaly detection algorithms and return results."""
    volume_anomalies = detect_volume_anomalies(articles)
    sentiment_anomalies = detect_sentiment_anomalies(articles)
    shift_anomalies = detect_sector_shift_anomalies(articles)

    all_anomalies = volume_anomalies + sentiment_anomalies + shift_anomalies
    all_anomalies.sort(key=lambda x: abs(x.get("z_score", 0)), reverse=True)

    critical = [a for a in all_anomalies if a["severity"] == "critical"]
    warnings = [a for a in all_anomalies if a["severity"] == "warning"]

    logger.info("Anomaly detection: %d critical, %d warnings from %d articles",
                len(critical), len(warnings), len(articles))

    return {
        "anomalies": all_anomalies[:20],  # Top 20 anomalies
        "critical_count": len(critical),
        "warning_count": len(warnings),
        "total_detected": len(all_anomalies),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

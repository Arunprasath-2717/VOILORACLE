"""
VEILORACLE — Trend Forecasting Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uses linear regression on historical sentiment data to predict future trend direction.
Provides per-sector momentum indicators and forecast confidence.
"""

import logging
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger("veiloracle.trends")


def compute_trend(values: list[float]) -> dict:
    """Compute linear trend from a time series of sentiment values."""
    if len(values) < 2:
        return {"slope": 0.0, "direction": "stable", "confidence": 0.0, "forecast": 0.0}

    x = np.arange(len(values), dtype=float)
    y = np.array(values, dtype=float)

    # Linear regression: y = mx + b
    n = len(x)
    x_mean = x.mean()
    y_mean = y.mean()

    num = np.sum((x - x_mean) * (y - y_mean))
    den = np.sum((x - x_mean) ** 2)

    if den == 0:
        return {"slope": 0.0, "direction": "stable", "confidence": 0.0, "forecast": y_mean}

    slope = num / den
    intercept = y_mean - slope * x_mean

    # R-squared for confidence
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    r_squared = max(0.0, min(1.0, r_squared))

    # Forecast next value
    forecast = slope * (n) + intercept

    # Direction
    if slope > 0.02:
        direction = "rising"
    elif slope < -0.02:
        direction = "falling"
    else:
        direction = "stable"

    return {
        "slope": round(float(slope), 4),
        "direction": direction,
        "confidence": round(float(r_squared), 3),
        "forecast": round(float(forecast), 4),
        "data_points": n
    }


def compute_momentum(values: list[float], window: int = 5) -> dict:
    """Compute momentum (rate of change) for a sequence."""
    if len(values) < 2:
        return {"momentum": 0.0, "acceleration": 0.0}

    recent = values[-window:] if len(values) >= window else values
    older = values[:-window] if len(values) > window else values[:1]

    recent_avg = sum(recent) / len(recent) if recent else 0
    older_avg = sum(older) / len(older) if older else 0
    momentum = recent_avg - older_avg

    # Acceleration (change in momentum)
    if len(values) >= 3:
        mid = len(values) // 2
        first_half = values[:mid]
        second_half = values[mid:]
        m1 = (sum(second_half) / len(second_half)) - (sum(first_half) / len(first_half))
        acceleration = m1
    else:
        acceleration = 0.0

    return {
        "momentum": round(float(momentum), 4),
        "acceleration": round(float(acceleration), 4)
    }


def analyze_sector_trends(articles: list[dict]) -> dict:
    """
    Analyze sentiment trends per sector.
    Returns dict of sector -> trend_data.
    """
    sector_sentiments = defaultdict(list)

    for article in articles:
        sentiment_score = article.get("sentiment", {}).get("compound", 0.0)
        for impact in article.get("impacts", []):
            sector = impact["sector"]
            sector_sentiments[sector].append(sentiment_score)

    trends = {}
    for sector, values in sector_sentiments.items():
        if len(values) < 2:
            continue
        trend = compute_trend(values)
        momentum = compute_momentum(values)
        trends[sector] = {
            **trend,
            **momentum,
            "current_sentiment": round(float(values[-1]) if values else 0.0, 4),
            "avg_sentiment": round(float(sum(values) / len(values)), 4),
        }

    # Sort by absolute slope (most dynamic sectors first)
    sorted_sectors = sorted(trends.items(), key=lambda x: abs(x[1]["slope"]), reverse=True)
    trends = dict(sorted_sectors)

    logger.info("Trend analysis: %d sectors analyzed.", len(trends))
    return trends


def get_top_movers(trends: dict, top_n: int = 10) -> dict:
    """Get top rising and falling sectors."""
    rising = sorted(
        [(s, t) for s, t in trends.items() if t["direction"] == "rising"],
        key=lambda x: x[1]["slope"], reverse=True
    )[:top_n]

    falling = sorted(
        [(s, t) for s, t in trends.items() if t["direction"] == "falling"],
        key=lambda x: x[1]["slope"]
    )[:top_n]

    return {
        "rising": [{"sector": s, **t} for s, t in rising],
        "falling": [{"sector": s, **t} for s, t in falling],
        "total_analyzed": len(trends)
    }

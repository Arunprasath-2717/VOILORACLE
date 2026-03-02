"""
VEILORACLE - Intelligence Engine
Calculates importance, risk, and sector impacts for events.
"""

import json
import logging

logger = logging.getLogger("veiloracle.intelligence")


def _round_1dp(value: float) -> float:
    """Round to 1 decimal place without using round(x, ndigits)."""
    return float(int(value * 10 + 0.5)) / 10.0


def _get_top_n(items: list, n: int) -> list:
    """Get first n items from a list without slicing."""
    result = []
    for i in range(min(n, len(items))):
        result.append(items[i])
    return result


def _find_dominant(bullish: int, bearish: int, neutral: int) -> str:
    """Find the dominant direction from counts."""
    if bullish >= bearish and bullish >= neutral:
        return "Bullish"
    if bearish >= bullish and bearish >= neutral:
        return "Bearish"
    return "Neutral"


def compute_intelligence(events: list, articles: list) -> list:
    """Enhance events with intelligence metrics."""
    for event in events:
        indices = event.get("article_indices", [])
        cluster_articles = []
        for i in indices:
            if i < len(articles):
                cluster_articles.append(articles[i])

        if not cluster_articles:
            event["importance_score"] = 0.0
            event["risk_score"] = 0.0
            event["impact_json"] = "[]"
            continue

        # 1. Importance Score (0-100)
        size_val = int(event.get("size", 1))
        size_factor = float(min(size_val * 5, 60))

        total_intensity = 0.0
        count = 0
        for a in cluster_articles:
            s = a.get("sentiment")
            if s is None:
                s = {}
            compound = s.get("compound", 0)
            total_intensity += abs(float(compound))
            count += 1

        avg_intensity = total_intensity / count if count > 0 else 0.0
        intensity_factor = avg_intensity * 40.0

        importance = _round_1dp(size_factor + intensity_factor)
        if importance > 100.0:
            importance = 100.0
        event["importance_score"] = importance

        # 2. Risk Score (0-100)
        neg_count = 0
        for a in cluster_articles:
            s = a.get("sentiment")
            if s is None:
                s = {}
            if s.get("label") == "Negative":
                neg_count += 1

        total_articles = len(cluster_articles)
        neg_ratio = float(neg_count) / float(total_articles) if total_articles > 0 else 0.0
        risk = _round_1dp(neg_ratio * 100.0)
        event["risk_score"] = risk

        # 3. Sector Impacts
        # Use parallel lists instead of nested dicts to avoid Pyre2 issues
        sector_names: list = []
        sector_bullish: list = []
        sector_bearish: list = []
        sector_neutral: list = []

        for a in cluster_articles:
            impact_list = a.get("impacts", [])
            for imp in impact_list:
                sector = str(imp.get("sector", "Unknown"))
                raw_direction = str(imp.get("direction", "Neutral"))

                if "Bullish" in raw_direction:
                    direction = "Bullish"
                elif "Bearish" in raw_direction:
                    direction = "Bearish"
                else:
                    direction = "Neutral"

                # Find or create sector entry
                idx = -1
                for si in range(len(sector_names)):
                    if sector_names[si] == sector:
                        idx = si
                        break

                if idx == -1:
                    sector_names.append(sector)
                    sector_bullish.append(0)
                    sector_bearish.append(0)
                    sector_neutral.append(0)
                    idx = len(sector_names) - 1

                if direction == "Bullish":
                    sector_bullish[idx] = sector_bullish[idx] + 1
                elif direction == "Bearish":
                    sector_bearish[idx] = sector_bearish[idx] + 1
                else:
                    sector_neutral[idx] = sector_neutral[idx] + 1

        impact_summary = []
        for si in range(len(sector_names)):
            b = int(sector_bullish[si])
            be = int(sector_bearish[si])
            n = int(sector_neutral[si])
            dominant = _find_dominant(b, be, n)
            impact_summary.append({
                "sector": sector_names[si],
                "direction": dominant,
                "count": b + be + n
            })

        # Sort by impact count (descending)
        impact_summary.sort(key=lambda x: -int(x.get("count", 0)))

        # Top 3 sectors
        top_impacts = _get_top_n(impact_summary, 3)
        event["impact_json"] = json.dumps(top_impacts)

    return events

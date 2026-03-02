"""
VEILORACLE - Intelligence Engine
Calculates importance, risk, and sector impacts for events.
"""

import json
import logging

logger = logging.getLogger("veiloracle.intelligence")


def _round_1dp(value):
    """Round to 1 decimal place without using round(x, ndigits)."""
    return float(int(value * 10 + 0.5)) / 10.0


def _get_top_n(items, n):
    """Get first n items from a list without slicing."""
    result = []
    count = len(items)
    if n < count:
        count = n
    i = 0
    while i < count:
        result.append(items[i])
        i = i + 1
    return result


def _find_dominant(bullish, bearish, neutral):
    """Find the dominant direction from counts."""
    if bullish >= bearish and bullish >= neutral:
        return "Bullish"
    if bearish >= bullish and bearish >= neutral:
        return "Bearish"
    return "Neutral"


def compute_intelligence(events, articles):
    """Enhance events with intelligence metrics."""
    event_idx = 0
    while event_idx < len(events):
        event = events[event_idx]
        indices = event.get("article_indices", [])
        cluster_articles = []
        j = 0
        while j < len(indices):
            idx = indices[j]
            if idx < len(articles):
                cluster_articles.append(articles[idx])
            j = j + 1

        if len(cluster_articles) == 0:
            event["importance_score"] = 0.0
            event["risk_score"] = 0.0
            event["impact_json"] = "[]"
            event_idx = event_idx + 1
            continue

        # 1. Importance Score (0-100)
        size_val = int(event.get("size", 1))
        size_capped = size_val * 5
        if size_capped > 60:
            size_capped = 60
        size_factor = float(size_capped)

        total_intensity = 0.0
        art_count = 0
        k = 0
        while k < len(cluster_articles):
            a = cluster_articles[k]
            s = a.get("sentiment")
            if s is None:
                s = {}
            compound = float(s.get("compound", 0))
            if compound < 0:
                compound = -compound
            total_intensity = total_intensity + compound
            art_count = art_count + 1
            k = k + 1

        avg_intensity = 0.0
        if art_count > 0:
            avg_intensity = total_intensity / float(art_count)
        intensity_factor = avg_intensity * 40.0

        importance = _round_1dp(size_factor + intensity_factor)
        if importance > 100.0:
            importance = 100.0
        event["importance_score"] = importance

        # 2. Risk Score (0-100)
        neg_count = 0
        k = 0
        while k < len(cluster_articles):
            a = cluster_articles[k]
            s = a.get("sentiment")
            if s is None:
                s = {}
            if s.get("label") == "Negative":
                neg_count = neg_count + 1
            k = k + 1

        total_articles = len(cluster_articles)
        neg_ratio = 0.0
        if total_articles > 0:
            neg_ratio = float(neg_count) / float(total_articles)
        risk = _round_1dp(neg_ratio * 100.0)
        event["risk_score"] = risk

        # 3. Sector Impacts
        sector_data = {}

        k = 0
        while k < len(cluster_articles):
            a = cluster_articles[k]
            impact_list = a.get("impacts", [])
            m = 0
            while m < len(impact_list):
                imp = impact_list[m]
                sector = str(imp.get("sector", "Unknown"))
                raw_direction = str(imp.get("direction", "Neutral"))

                if "Bullish" in raw_direction:
                    direction = "Bullish"
                elif "Bearish" in raw_direction:
                    direction = "Bearish"
                else:
                    direction = "Neutral"

                if sector not in sector_data:
                    sector_data[sector] = {"Bullish": 0, "Bearish": 0, "Neutral": 0}

                entry = sector_data[sector]
                entry[direction] = entry[direction] + 1

                m = m + 1
            k = k + 1

        impact_summary = []
        for sector_name in sector_data:
            entry = sector_data[sector_name]
            b_val = int(entry.get("Bullish", 0))
            be_val = int(entry.get("Bearish", 0))
            n_val = int(entry.get("Neutral", 0))
            dominant = _find_dominant(b_val, be_val, n_val)
            impact_summary.append({
                "sector": sector_name,
                "direction": dominant,
                "count": b_val + be_val + n_val
            })

        # Sort by impact count (descending) using simple bubble sort
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(impact_summary) - 1:
                if int(impact_summary[i].get("count", 0)) < int(impact_summary[i + 1].get("count", 0)):
                    tmp = impact_summary[i]
                    impact_summary[i] = impact_summary[i + 1]
                    impact_summary[i + 1] = tmp
                    changed = True
                i = i + 1

        # Top 3 sectors
        top_impacts = _get_top_n(impact_summary, 3)
        event["impact_json"] = json.dumps(top_impacts)

        event_idx = event_idx + 1

    return events

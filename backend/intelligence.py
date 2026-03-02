"""
VEILORACLE - Intelligence Engine
Calculates importance, risk, and sector impacts for events.
Fully Pyre-safe version.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger("veiloracle.intelligence")


# ---------- Utilities ----------

def _round_1dp(value: float) -> float:
    """Round to 1 decimal place without using round(x, ndigits)."""
    return float(int(value * 10 + 0.5)) / 10.0


def _get_top_n(items: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    """Return first n items safely."""
    result: List[Dict[str, Any]] = []

    count = len(items)

    if n < count:
        count = n

    i = 0
    while i < count:
        result.append(items[i])
        i = i + 1

    return result


def _find_dominant(bullish: int, bearish: int, neutral: int) -> str:

    if bullish >= bearish and bullish >= neutral:
        return "Bullish"

    if bearish >= bullish and bearish >= neutral:
        return "Bearish"

    return "Neutral"


# ---------- Core Engine ----------

def compute_intelligence(
    events: List[Dict[str, Any]],
    articles: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    event_idx = 0

    while event_idx < len(events):

        event: Dict[str, Any] = events[event_idx]

        # ---------- Article Index Handling ----------

        raw_indices = event.get("article_indices", [])

        if isinstance(raw_indices, list):
            indices: List[int] = raw_indices
        else:
            indices = []

        cluster_articles: List[Dict[str, Any]] = []

        j = 0

        while j < len(indices):

            idx_val = indices[j]  # type: ignore

            if isinstance(idx_val, int):

                if idx_val < len(articles):
                    cluster_articles.append(articles[idx_val])  # type: ignore

            j = j + 1

        # ---------- Empty Cluster ----------

        if len(cluster_articles) == 0:

            event["importance_score"] = 0.0
            event["risk_score"] = 0.0
            event["impact_json"] = []

            event_idx = event_idx + 1
            continue

        # ---------- Importance Score ----------

        size_val = int(event.get("size", 1))

        size_factor_val = size_val * 3

        if size_factor_val > 60:
            size_factor_val = 60

        size_factor = float(size_factor_val)

        total_intensity = 0.0
        art_count = 0

        k = 0

        while k < len(cluster_articles):

            article: Dict[str, Any] = cluster_articles[k]

            sentiment = article.get("sentiment", {})

            if not isinstance(sentiment, dict):
                sentiment = {}

            compound_val = sentiment.get("compound", 0)

            try:
                compound = float(compound_val)
            except Exception:
                compound = 0.0

            if compound < 0:
                compound = compound * -1.0

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

        # ---------- Risk Score ----------

        neg_count = 0

        k = 0

        while k < len(cluster_articles):

            article = cluster_articles[k]

            sentiment = article.get("sentiment", {})

            if isinstance(sentiment, dict):

                if sentiment.get("label") == "Negative":
                    neg_count = neg_count + 1  # type: ignore

            k = k + 1

        total_articles = len(cluster_articles)

        neg_ratio = 0.0

        if total_articles > 0:
            neg_ratio = float(neg_count) / float(total_articles)

        risk = _round_1dp(neg_ratio * 100.0)

        if risk > 100:
            risk = 100.0

        event["risk_score"] = risk

        # ---------- Sector Impacts ----------

        sector_data: Dict[str, Dict[str, int]] = {}

        k = 0

        while k < len(cluster_articles):

            article = cluster_articles[k]

            raw_impacts = article.get("impacts", [])

            if isinstance(raw_impacts, list):
                impact_list: List[Dict[str, Any]] = raw_impacts
            else:
                impact_list = []

            m = 0

            while m < len(impact_list):

                imp = impact_list[m]  # type: ignore

                if isinstance(imp, dict):

                    sector_val = imp.get("sector", "Unknown")
                    sector = str(sector_val)

                    direction_val = imp.get("direction", "Neutral")
                    raw_direction = str(direction_val)

                    if "Bullish" in raw_direction:
                        direction = "Bullish"

                    elif "Bearish" in raw_direction:
                        direction = "Bearish"

                    else:
                        direction = "Neutral"

                    if sector not in sector_data:

                        sector_data[sector] = {
                            "Bullish": 0,
                            "Bearish": 0,
                            "Neutral": 0
                        }

                    entry: Dict[str, int] = sector_data[sector]  # type: ignore

                    entry[direction] = entry[direction] + 1  # type: ignore

                m = m + 1

            k = k + 1  # type: ignore

        # ---------- Impact Summary ----------

        impact_summary: List[Dict[str, Any]] = []

        for sector_name in sector_data:

            entry: Dict[str, int] = sector_data[sector_name]

            b_val = int(entry["Bullish"])
            be_val = int(entry["Bearish"])
            n_val = int(entry["Neutral"])

            dominant = _find_dominant(b_val, be_val, n_val)

            impact_summary.append({
                "sector": sector_name,
                "direction": dominant,
                "count": b_val + be_val + n_val
            })

        # Safe sorting

        impact_summary.sort(
            key=lambda x: int(x.get("count", 0)),
            reverse=True
        )

        top_impacts = _get_top_n(impact_summary, 3)

        event["impact_json"] = top_impacts

        event_idx = event_idx + 1

    return events
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger("veiloracle.intelligence")


def _round_1dp(value: float) -> float:
    return float(int(value * 10 + 0.5)) / 10.0


def _get_top_n(items: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    count = len(items)

    if n < count:
        count = n

    i = 0
    while i < count:
        result.append(items[i])
        i += 1

    return result


def _find_dominant(bullish: int, bearish: int, neutral: int) -> str:

    if bullish >= bearish and bullish >= neutral:
        return "Bullish"

    if bearish >= bullish and bearish >= neutral:
        return "Bearish"

    return "Neutral"


def compute_intelligence(
    events: List[Dict[str, Any]],
    articles: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    event_idx = 0

    while event_idx < len(events):

        event: Dict[str, Any] = events[event_idx]

        indices: List[int] = event.get("article_indices", [])

        cluster_articles: List[Dict[str, Any]] = []

        j = 0

        while j < len(indices):

            idx = indices[j]

            if isinstance(idx, int) and idx < len(articles):
                cluster_articles.append(articles[idx])

            j += 1

        if len(cluster_articles) == 0:

            event["importance_score"] = 0.0
            event["risk_score"] = 0.0
            event["impact_json"] = []

            event_idx += 1
            continue

        # Importance Score

        size_val = int(event.get("size", 1))

        size_capped = size_val * 3

        if size_capped > 60:
            size_capped = 60

        size_factor = float(size_capped)

        total_intensity = 0.0
        art_count = 0

        k = 0

        while k < len(cluster_articles):

            a: Dict[str, Any] = cluster_articles[k]

            s: Dict[str, Any] = a.get("sentiment", {})

            compound = float(s.get("compound", 0))

            if compound < 0:
                compound = -compound

            total_intensity += compound
            art_count += 1

            k += 1

        avg_intensity = 0.0

        if art_count > 0:
            avg_intensity = total_intensity / float(art_count)

        intensity_factor = avg_intensity * 40.0

        importance = _round_1dp(size_factor + intensity_factor)

        if importance > 100.0:
            importance = 100.0

        event["importance_score"] = importance

        # Risk Score

        neg_count = 0

        k = 0

        while k < len(cluster_articles):

            a = cluster_articles[k]

            s: Dict[str, Any] = a.get("sentiment", {})

            if s.get("label") == "Negative":
                neg_count += 1

            k += 1

        total_articles = len(cluster_articles)

        neg_ratio = 0.0

        if total_articles > 0:
            neg_ratio = float(neg_count) / float(total_articles)

        risk = _round_1dp(neg_ratio * 100.0)

        event["risk_score"] = risk

        # Sector Impact

        sector_data: Dict[str, Dict[str, int]] = {}

        k = 0

        while k < len(cluster_articles):

            a = cluster_articles[k]

            impact_list: List[Dict[str, Any]] = a.get("impacts", [])

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

                    sector_data[sector] = {
                        "Bullish": 0,
                        "Bearish": 0,
                        "Neutral": 0
                    }

                sector_data[sector][direction] += 1

                m += 1

            k += 1

        impact_summary: List[Dict[str, Any]] = []

        for sector_name in sector_data:

            entry = sector_data[sector_name]

            b_val = entry["Bullish"]
            be_val = entry["Bearish"]
            n_val = entry["Neutral"]

            dominant = _find_dominant(b_val, be_val, n_val)

            impact_summary.append({
                "sector": sector_name,
                "direction": dominant,
                "count": b_val + be_val + n_val
            })

        impact_summary.sort(
            key=lambda x: x["count"],
            reverse=True
        )

        top_impacts = _get_top_n(impact_summary, 3)

        event["impact_json"] = top_impacts

        event_idx += 1

    return events
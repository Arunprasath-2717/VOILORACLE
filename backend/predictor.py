"""
VEILORACLE — Impact Predictor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rule-based sector impact prediction.
"""

import logging
from backend import config

logger = logging.getLogger("veiloracle.predictor")


def match_sectors(text: str) -> list[dict]:
    text_lower = text.lower()
    matches = []
    for sector, keywords in config.SECTOR_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text_lower]
        if matched:
            matches.append({"sector": sector, "matched_keywords": matched,
                            "confidence": round(min(len(matched) / 3.0, 1.0), 3)})
    matches.sort(key=lambda m: -m["confidence"])
    return matches


def predict_direction(sentiment_label: str, sentiment_compound: float) -> dict:
    a = abs(sentiment_compound)
    strength = "Strong" if a >= 0.6 else "Moderate" if a >= 0.3 else "Mild" if a >= 0.05 else "Neutral"
    if sentiment_label == "Positive":
        return {"direction": "↑ Bullish", "icon": "↑", "strength": strength}
    elif sentiment_label == "Negative":
        return {"direction": "↓ Bearish", "icon": "↓", "strength": strength}
    return {"direction": "→ Neutral", "icon": "→", "strength": "Neutral"}


def predict_impact(article: dict) -> list[dict]:
    text = article.get("clean_text", f"{article.get('title','')} {article.get('description','')}")
    sentiment = article.get("sentiment", {"label": "Neutral", "compound": 0.0})
    direction_info = predict_direction(sentiment["label"], sentiment["compound"])
    return [{"sector": m["sector"], "direction": direction_info["direction"], "icon": direction_info["icon"],
             "strength": direction_info["strength"], "confidence": m["confidence"],
             "matched_keywords": m["matched_keywords"]} for m in match_sectors(text)]


def predict_impacts(articles: list[dict]) -> list[dict]:
    total = 0
    for article in articles:
        impacts = predict_impact(article)
        article["impacts"] = impacts
        total += len(impacts)
    logger.info("Impact prediction: %d sector impacts across %d articles", total, len(articles))
    return articles


def summarize_sector_impacts(articles: list[dict]) -> dict:
    summary = {}
    for article in articles:
        for impact in article.get("impacts", []):
            s = impact["sector"]
            if s not in summary:
                summary[s] = {"total_mentions": 0, "bullish": 0, "bearish": 0, "neutral": 0, "confidences": []}
            summary[s]["total_mentions"] += 1
            summary[s]["confidences"].append(impact["confidence"])
            if "Bullish" in impact["direction"]: summary[s]["bullish"] += 1
            elif "Bearish" in impact["direction"]: summary[s]["bearish"] += 1
            else: summary[s]["neutral"] += 1
    for s, d in summary.items():
        d["avg_confidence"] = round(sum(d["confidences"]) / len(d["confidences"]), 3) if d["confidences"] else 0
        del d["confidences"]
        d["net_direction"] = "↑ Bullish" if d["bullish"] > d["bearish"] else "↓ Bearish" if d["bearish"] > d["bullish"] else "→ Mixed"
    return summary

"""
Kronaxis — Sentiment Analyzer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VADER sentiment analysis for articles and events.
"""

import logging
from backend import config

logger = logging.getLogger("Kronaxis.sentiment")

_analyzer = None


def _get_analyzer():
    global _analyzer
    if _analyzer is None:
        # Check for light mode to prevent OOM
        if os.environ.get("KRONAXIS_LIGHT_MODE") == "true":
            logger.info("KRONAXIS_LIGHT_MODE is enabled. Using keyword-based sentiment.")
            _analyzer = "fallback"
            return _analyzer

        try:
            from transformers import pipeline
            logger.info("Loading RoBERTa sentiment model...")
            _analyzer = pipeline(
                "sentiment-analysis", 
                model="cardiffnlp/twitter-roberta-base-sentiment",
                device=-1  # Use CPU; replace with 0 if GPU is available
            )
        except Exception as e:
            logger.warning("Transformers not available (%s), using keyword fallback.", e)
            _analyzer = "fallback"
    return _analyzer


def _keyword_sentiment(text: str) -> dict:
    """Simple keyword-based sentiment fallback."""
    pos_words = {"surge", "gain", "growth", "jump", "record", "profit", "bullish", "success", "victory", "win", "improved", "strong", "positive", "high"}
    neg_words = {"crash", "plunge", "loss", "decline", "fall", "debt", "bearish", "crisis", "fail", "deficit", "weak", "negative", "low", "war", "conflict"}
    
    words = set(text.lower().split())
    pos_count = len(words & pos_words)
    neg_count = len(words & neg_words)
    
    if pos_count > neg_count:
        label = "Positive"
        compound = 0.5 + (0.1 * min(pos_count - neg_count, 5))
    elif neg_count > pos_count:
        label = "Negative"
        compound = -0.5 - (0.1 * min(neg_count - pos_count, 5))
    else:
        label = "Neutral"
        compound = 0.0
        
    return {"label": label, "compound": float(compound), "scores": {"pos": pos_count, "neg": neg_count}}


def analyze_sentiment(text: str) -> dict:
    """Returns {label, compound, scores}."""
    if not text:
        return {"label": "Neutral", "compound": 0.0, "scores": {}}

    analyzer = _get_analyzer()
    if analyzer == "fallback":
        return _keyword_sentiment(text)
    
    try:
        short_text = text[:1500]
        result = analyzer(short_text)[0]
        # cardiffnlp/twitter-roberta-base-sentiment returns LABEL_0 (negative), LABEL_1 (neutral), LABEL_2 (positive)
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        label = label_map.get(result["label"], "Neutral")
        
        # Approximate compound score [-1.0 to 1.0] from the confidence score
        score = result["score"]
        if label == "Positive":
            c = score
        elif label == "Negative":
            c = -score
        else:
            c = 0.0
            
        return {"label": label, "compound": c, "scores": result}
    except Exception as e:
        logger.error("Sentiment analysis failed: %s", e)
        return _keyword_sentiment(text)


def analyze_articles(articles: list[dict]) -> list[dict]:
    """Add 'sentiment' field to each article."""
    pos = neg = neu = 0
    for article in articles:
        text = article.get("clean_text", f"{article.get('title','')} {article.get('description','')}")
        sentiment = analyze_sentiment(text)
        article["sentiment"] = sentiment
        if sentiment["label"] == "Positive": pos += 1
        elif sentiment["label"] == "Negative": neg += 1
        else: neu += 1
    logger.info("Sentiment: %d positive, %d negative, %d neutral", pos, neg, neu)
    return articles


def analyze_event_sentiment(event: dict, articles: list[dict]) -> dict:
    """Aggregate sentiment for an event."""
    compounds = []
    pos = neg = neu = 0
    for idx in event.get("article_indices", []):
        if idx < len(articles):
            s = articles[idx].get("sentiment", analyze_sentiment(articles[idx].get("clean_text", "")))
            compounds.append(s["compound"])
            if s["label"] == "Positive": pos += 1
            elif s["label"] == "Negative": neg += 1
            else: neu += 1
    avg = sum(compounds) / len(compounds) if compounds else 0.0
    label = "Positive" if avg >= 0.05 else "Negative" if avg <= -0.05 else "Neutral"
    return {"label": label, "compound": round(avg, 4), "positive_count": pos, "negative_count": neg, "neutral_count": neu}

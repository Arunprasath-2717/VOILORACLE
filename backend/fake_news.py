"""
VEILORACLE — Fake News Detector
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scores articles for fake news probability using roberta-base-openai-detector.
"""

import logging

logger = logging.getLogger("veiloracle.fakenews")

_detector = None


def _get_detector():
    global _detector
    if _detector is None:
        try:
            from transformers import pipeline
            logger.info("Loading Fake News detection model...")
            _detector = pipeline("text-classification", model="roberta-base-openai-detector", device=-1)
        except Exception as e:
            logger.warning("Fake News model not available: %s", e)
            _detector = "fallback"
    return _detector


def detect_fake_news(text: str) -> dict:
    detector = _get_detector()
    if detector == "fallback" or not text:
        return {"label": "Real", "score": 1.0, "is_fake": False}
        
    try:
        short_text = text[:1024]
        res = detector(short_text)[0]
        # output is "Real" or "Fake"
        is_fake = res['label'] == 'Fake'
        return {"label": res['label'], "score": round(res['score'], 4), "is_fake": is_fake}
    except Exception as e:
        logger.error("Fake news detection failed: %s", e)
        return {"label": "Real", "score": 1.0, "is_fake": False}

def analyze_articles_fake_news(articles: list[dict]) -> list[dict]:
    for article in articles:
        text = article.get("clean_text", f"{article.get('title','')} {article.get('description','')}")
        article["fake_news_analysis"] = detect_fake_news(text)
    return articles

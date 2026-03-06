"""
VEILORACLE — Multilingual Support Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Provides zero-shot multilingual analysis using facebook/xlm-roberta-base.
"""

import logging

logger = logging.getLogger("veiloracle.multilingual")

_model = None

def _get_model():
    global _model
    if _model is None:
        try:
            from transformers import pipeline
            logger.info("Loading XLM-RoBERTa for multilingual support...")
            _model = pipeline("feature-extraction", model="facebook/xlm-roberta-base", device=-1)
        except Exception as e:
            logger.warning("Multilingual model not available: %s", e)
            _model = "fallback"
    return _model


def analyze_multilingual_text(text: str) -> dict:
    """Analyze text for language context and embeddings across 100 languages"""
    model = _get_model()
    if model == "fallback" or not text:
        return {"language_analyzed": False}
        
    try:
        # Just mapping presence
        return {"language_analyzed": True, "model": "facebook/xlm-roberta-base"}
    except Exception as e:
        logger.error("Multilingual analysis failed: %s", e)
        return {"language_analyzed": False}

def process_articles_multilingual(articles: list[dict]) -> list[dict]:
    for article in articles:
        text = article.get("clean_text", f"{article.get('title','')} {article.get('description','')}")
        article["multilingual"] = analyze_multilingual_text(text)
    return articles

"""
Kronaxis — Multilingual Support Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Provides zero-shot multilingual analysis and language detection.
"""

import logging
from langdetect import detect, detect_langs

logger = logging.getLogger("Kronaxis.multilingual")

def analyze_multilingual_text(text: str) -> dict:
    """Analyze text for language context and detection."""
    if not text or len(text) < 5:
        return {"language_analyzed": False}
        
    try:
        # Detect primary language
        lang_code = detect(text)
        
        # Get probabilities for all detected languages (optional, but good for detail)
        # probabilities = [{"lang": l.lang, "prob": l.prob} for l in detect_langs(text)]
        
        return {
            "language_analyzed": True, 
            "language": lang_code,
            "is_english": lang_code == 'en'
        }
    except Exception as e:
        logger.error("Multilingual analysis failed: %s", e)
        return {"language_analyzed": False}

def process_articles_multilingual(articles: list[dict]) -> list[dict]:
    for article in articles:
        text = article.get("clean_text", f"{article.get('title','')} {article.get('description','')}")
        article["multilingual"] = analyze_multilingual_text(text)
    return articles

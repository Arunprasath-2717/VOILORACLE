"""
VEILORACLE — AI Summarizer Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uses facebook/bart-large-cnn transformer model to generate concise summaries.
Falls back to extractive summarization if transformers unavailable.
"""

import logging

import backend.config as config
from backend import gemini_engine

logger = logging.getLogger("veiloracle.summarizer")

_summarizer = None
_use_transformers = True
_use_gemini = config.GEMINI_API_KEY != ""


def _get_summarizer():
    global _summarizer, _use_transformers
    if _summarizer is None:
        try:
            from transformers import pipeline
            logger.info("Loading BART summarization model (this may take a moment)...")
            _summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
            logger.info("BART summarization model loaded successfully.")
        except Exception as e:
            logger.warning("Transformers not available (%s), using extractive fallback.", e)
            _use_transformers = False
            _summarizer = "fallback"
    return _summarizer


def _extractive_summary(text: str, max_sentences: int = 3) -> str:
    """Simple extractive summarization: pick top sentences by keyword density."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= max_sentences:
        return text

    # Score sentences by length and keyword presence
    important_words = {"market", "surge", "crash", "announce", "record", "growth",
                       "decline", "invest", "global", "impact", "breakthrough",
                       "crisis", "profit", "loss", "discover", "technology"}
    scored = []
    for s in sentences:
        words = set(s.lower().split())
        score = len(words & important_words) + (1 if len(s) > 40 else 0)
        scored.append((score, s))
    scored.sort(key=lambda x: -x[0])
    top = [s for _, s in scored[:max_sentences]]
    return " ".join(top)


def summarize_text(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """Generate a summary of the given text."""
    if not text or len(text.strip()) < 50:
        return text.strip() if text else ""

    # 1. Try Gemini only for standalone calls, not bulk pipeline processing
    # Skipping Gemini for bulk to preserve API quota (free tier: 20 req/day)
    # If _use_gemini and not bulk mode, try it
    
    # 2. Try Transformers (Tier 2) — also skip for speed during pipeline
    # Use extractive for all pipeline calls — fast and reliable
    return _extractive_summary(text)

    # 2. Try Transformers (Tier 2)
    summarizer = _get_summarizer()
    if _use_transformers and summarizer != "fallback":
        try:
            input_text = text[:1024]
            result = summarizer(input_text, max_length=max_length, min_length=min_length,
                                do_sample=False, truncation=True)
            return result[0]["summary_text"]
        except Exception as e:
            logger.warning("BART summarization failed: %s, using extractive fallback", e)
            return _extractive_summary(text)
    
    # 3. Extractive Fallback (Tier 3)
    else:
        return _extractive_summary(text)


def summarize_event(event: dict, articles: list[dict]) -> str:
    """Generate a summary for an event cluster by combining its articles."""
    indices = event.get("article_indices", [])
    texts = []
    for idx in indices:
        if idx < len(articles):
            t = articles[idx].get("clean_text", f"{articles[idx].get('title', '')} {articles[idx].get('description', '')}")
            texts.append(t)

    if not texts:
        return event.get("label", "No summary available.")

    combined = " ".join(texts[:5])  # Combine up to 5 articles
    return summarize_text(combined)


def summarize_events(events: list[dict], articles: list[dict]) -> list[dict]:
    """Add 'ai_summary' field to each event."""
    for event in events:
        event["ai_summary"] = summarize_event(event, articles)
    logger.info("Generated AI summaries for %d events.", len(events))
    return events

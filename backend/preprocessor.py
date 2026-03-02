"""
VEILORACLE — Text Preprocessor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cleans and normalizes text for NLP processing.
"""

import logging
import re
import string

logger = logging.getLogger("veiloracle.preprocessor")

_nltk_ready = False


def _ensure_nltk():
    global _nltk_ready
    if _nltk_ready:
        return
    import nltk
    for resource in ["punkt", "punkt_tab", "stopwords"]:
        try:
            nltk.data.find(f"tokenizers/{resource}" if "punkt" in resource else f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)
    _nltk_ready = True


def clean_text(text: str) -> str:
    """Full cleaning: HTML → URLs → lowercase → special chars → whitespace."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)        # strip HTML
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  # remove URLs
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s.,!?'-]", " ", text)  # remove special chars
    text = re.sub(r"\s+", " ", text).strip()     # normalize whitespace
    return text


def tokenize_and_filter(text: str) -> list[str]:
    """Tokenize and remove stopwords."""
    _ensure_nltk()
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    return [t for t in tokens if t not in stop_words and t not in string.punctuation and len(t) > 2]


def preprocess_articles(articles: list[dict]) -> list[dict]:
    """Add 'clean_text' and 'tokens' fields to each article."""
    _ensure_nltk()
    for article in articles:
        raw = f"{article.get('title', '')}. {article.get('description', '')}"
        article["clean_text"] = clean_text(raw)
        article["tokens"] = tokenize_and_filter(article["clean_text"])
    logger.info("Preprocessed %d articles.", len(articles))
    return articles

"""
VEILORACLE — Gemini AI Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interface for Google Gemini Flash to power chat and summaries.
Uses the new google-genai SDK (google.genai).
"""

import logging
from backend import config

logger = logging.getLogger("veiloracle.gemini")

DEFAULT_MODEL = "gemini-2.0-flash"
FALLBACK_MODELS = ["gemini-1.5-flash", "gemini-1.5-pro"]

_client = None


def _get_client():
    """Get or create the Gemini client (lazy init)."""
    global _client
    if _client is not None:
        return _client
    if not config.GEMINI_API_KEY:
        logger.warning("No GEMINI_API_KEY found.")
        return None
    try:
        from google import genai  # type: ignore
        _client = genai.Client(api_key=config.GEMINI_API_KEY)
        logger.info("Gemini client initialized (google-genai SDK).")
        return _client
    except Exception as e:
        logger.error("Failed to initialize Gemini client: %s", e)
        return None


def generate_response(prompt: str, system_instruction: str = "") -> str:
    """Generate a response using Gemini with automatic model fallback."""
    client = _get_client()
    if client is None:
        return "Gemini AI is not configured. Please add GEMINI_API_KEY to your .env file."

    full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt

    models_to_try = [DEFAULT_MODEL] + FALLBACK_MODELS
    last_error = None

    for model_name in models_to_try:
        try:
            from google.genai import types  # type: ignore
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
            )
            text = response.text
            if text:
                return text
        except Exception as e:
            last_error = e
            err_str = str(e)[:120]
            logger.warning("Model %s failed: %s. Trying next...", model_name, err_str)
            continue

    logger.error("All Gemini models failed. Last error: %s", last_error)
    return f"Intelligence Core offline: {str(last_error)[:200]}"


def summarize_articles(text_blobs: list) -> str:
    """Summarize a collection of articles into an intelligence briefing."""
    limited = text_blobs[:10]
    combined_text = "\n\n".join(limited)
    prompt = (
        "Summarize the following news articles into a concise, professional "
        "intelligence briefing:\n\n" + combined_text
    )
    system_instruction = (
        "You are the VOILORACLE Intelligence Core. You provide sharp, "
        "data-driven summaries of global events."
    )
    return generate_response(prompt, system_instruction)

"""
VEILORACLE — Gemini AI Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interface for Google Gemini Flash 2.0 to power chat and summaries.
"""

import logging
import google.generativeai as genai
from backend import config

# Models confirmed available for this API key
DEFAULT_MODEL = "gemini-2.0-flash"
FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash-001"]

logger = logging.getLogger("veiloracle.gemini")

def init_gemini():
    if not config.GEMINI_API_KEY:
        logger.warning("No GEMINI_API_KEY found.")
        return False
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        return True
    except Exception as e:
        logger.error("Failed to initialize Gemini: %s", e)
        return False

def get_best_model():
    """Returns the preferred model."""
    return genai.GenerativeModel(model_name=DEFAULT_MODEL)

def generate_response(prompt: str, system_instruction: str = "") -> str:
    """Generate a response using Gemini with automatic model fallback."""
    if not init_gemini():
        return "Gemini AI is not configured."
    
    full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
    
    # Try the default model first, then fallbacks
    models_to_try = [DEFAULT_MODEL] + FALLBACK_MODELS
    last_error = None
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            last_error = e
            logger.warning("Model %s failed: %s. Trying next...", model_name, str(e)[:80])
            continue
    
    logger.error("All Gemini models failed. Last error: %s", last_error)
    return f"Error generating response: {str(last_error)}"

def summarize_articles(text_blobs: list[str]) -> str:
    """Summarize a collection of articles."""
    combined_text = "\n\n".join(text_blobs[:10]) # Limit to 10 articles
    prompt = f"Summarize the following news articles into a concise, professional intelligence briefing:\n\n{combined_text}"
    system_instruction = "You are the VOILORACLE Intelligence Core. You provide sharp, data-driven summaries of global events."
    return generate_response(prompt, system_instruction)

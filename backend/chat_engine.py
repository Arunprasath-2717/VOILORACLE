"""
Kronaxis — Conversational Intelligence Chat Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Allows users to ask natural-language questions about global events.
Uses local database context + Gemini API for response generation.
"""

import logging
import json
import re
from datetime import datetime

import requests  # type: ignore
import backend.config as config
from backend import database

logger = logging.getLogger("Kronaxis.chat")

SYSTEM_PROMPT = """You are Kronaxis AI, an elite real-time global intelligence analyst.
You have access to a live database of news articles collected from 8+ global OSINT sources.

CRITICAL INSTRUCTIONS:
1. You MUST ONLY respond to queries related to geopolitical events, global news, financial markets, sectors, and threats.
2. If the user asks a casual/conversational question (e.g., "how are you", "what is your name", "enough aah", "hi") or a question unrelated to news/intelligence, you MUST firmly politely decline to answer, stating that you are an intelligence analyst restricted to news analysis.
3. Your responses must be concise and analytical (like an intelligence briefing).
4. Back your analysis with data from the articles provided in context. Do not invent news.
5. Structure with bullet points or numbered lists when appropriate.
6. Include sentiment assessments and threat levels when relevant.
7. If no data matches the query, say so honestly.

Current UTC time: {timestamp}
Database contains {article_count} total articles.

CONTEXT — Recent articles matching the query:
{context}
"""


def _search_articles(query: str, limit: int = 20) -> list:
    """Search the local database for articles matching the query."""
    try:
        all_articles = database.get_recent_articles(300)
    except Exception:
        all_articles = []

    if not all_articles:
        return []

    query_lower = query.lower()
    query_words = set(re.findall(r'\b\w{3,}\b', query_lower))

    scored = []
    for a in all_articles:
        text = (
            str(a.get("title", "")) + " " +
            str(a.get("description", "")) + " " +
            str(a.get("source", ""))
        ).lower()

        # Simple keyword relevance scoring
        score = 0
        for word in query_words:
            if word in text:
                score += 1
                # Bonus for title match
                if word in str(a.get("title", "")).lower():
                    score += 2

        if score > 0:
            scored.append((score, a))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:limit]]


def _build_context(articles: list) -> str:
    """Build a text context block from matching articles."""
    if not articles:
        return "No matching articles found in the database."

    lines = []
    for i, a in enumerate(articles[:15], 1):
        title = a.get("title", "Unknown")
        source = a.get("source", "Unknown")
        sentiment = a.get("sentiment_label", "Neutral")
        published = a.get("published_at", "")
        desc = str(a.get("description", ""))[:200]

        lines.append(
            f"{i}. [{sentiment}] {title}\n"
            f"   Source: {source} | Published: {published}\n"
            f"   Summary: {desc}"
        )

    return "\n\n".join(lines)


def _call_gemini(prompt: str) -> str:
    """Call Google Gemini API for response generation."""
    api_key = config.GEMINI_API_KEY
    if not api_key:
        return _generate_local_response(prompt)

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1024,
                "topP": 0.8,
            }
        }
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "No response generated.")
        logger.warning("Gemini API returned status %d", resp.status_code)
    except Exception as e:
        logger.error("Gemini API error: %s", e)

    return _generate_local_response(prompt)


def _generate_local_response(prompt: str) -> str:
    """Fallback: generate a structured response locally without LLM."""
    # Extract context articles from the prompt
    context_start = prompt.find("CONTEXT")
    if context_start == -1:
        return "I don't have enough data to answer that question. Try running the intelligence pipeline first."

    context = prompt[context_start:]
    if "No matching articles found" in context:
        return ("🔍 No matching intelligence found in the current database.\n\n"
                "**Suggestions:**\n"
                "- Try broader search terms\n"
                "- Run the intelligence pipeline to collect fresh data\n"
                "- Check the Geo Intelligence tab for regional coverage")

    # Count articles referenced
    article_count = context.count("Source:")
    return (
        f"📊 **Intelligence Summary**\n\n"
        f"Found **{article_count} relevant articles** matching your query.\n\n"
        f"The articles span multiple sources and sentiment categories. "
        f"For detailed analysis, please review the Intelligence Feed and Analytics tabs.\n\n"
        f"*Note: Gemini API is not configured. Connect it for AI-powered natural language briefings.*"
    )


def process_chat_message(message: str) -> dict:
    """
    Process a user chat message and return an intelligence response.
    Returns: {"response": str, "sources": list, "timestamp": str}
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Search for relevant articles
    matching_articles = _search_articles(message)
    context = _build_context(matching_articles)

    try:
        article_count = database.get_article_count()
    except Exception:
        article_count = 0

    # Build the full prompt
    system = SYSTEM_PROMPT.format(
        timestamp=timestamp,
        article_count=article_count,
        context=context,
    )
    full_prompt = system + f"\n\nUSER QUESTION: {message}\n\nAnalyst Response:"

    # Generate response
    response_text = _call_gemini(full_prompt)

    # Build source references
    sources = []
    for a in matching_articles[:5]:
        sources.append({
            "title": a.get("title", ""),
            "source": a.get("source", ""),
            "sentiment": a.get("sentiment_label", "Neutral"),
            "url": a.get("url", ""),
        })

    return {
        "response": response_text,
        "sources": sources,
        "matching_articles": len(matching_articles),
        "timestamp": timestamp,
    }

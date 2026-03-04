"""
VEILORACLE — Model Router
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Routes articles to sector-specific AI models for deep analysis.
Fully Pyre2-safe version.

Sector → Model mapping:
  finance    → ProsusAI/finbert
  technology → Qwen/Qwen2-7B-Instruct
  politics   → mistralai/Mistral-7B-Instruct
  business   → deepseek-ai/deepseek-llm-7b-chat
  health     → microsoft/BioGPT-Large
  general    → meta-llama/Llama-3-8B-Instruct
"""

import logging
import os
from typing import List, Dict, Any, Optional

logger = logging.getLogger("veiloracle.model_router")

# ── Hugging Face API token for large model inference ─────────────────────────
HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")

# ── Model Registry ───────────────────────────────────────────────────────────
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "finance": {
        "model_id": "ProsusAI/finbert",
        "model_type": "local_pipeline",
        "pipeline_task": "sentiment-analysis",
        "description": "Financial sentiment detection, economic event interpretation, market impact estimation",
        "tasks": [
            "financial sentiment detection",
            "economic event interpretation",
            "market impact estimation",
        ],
    },
    "technology": {
        "model_id": "Qwen/Qwen2-7B-Instruct",
        "model_type": "hf_api",
        "description": "Summarize technology news, detect innovation trends, analyze impact on tech companies",
        "tasks": [
            "summarize technology news",
            "detect innovation trends",
            "analyze impact on tech companies",
        ],
    },
    "politics": {
        "model_id": "mistralai/Mistral-7B-Instruct-v0.3",
        "model_type": "hf_api",
        "description": "Analyze political events, detect geopolitical risk, interpret government policy",
        "tasks": [
            "analyze political events",
            "detect geopolitical risk",
            "interpret government policy",
        ],
    },
    "business": {
        "model_id": "deepseek-ai/deepseek-llm-7b-chat",
        "model_type": "hf_api",
        "description": "Analyze mergers and acquisitions, detect corporate strategy changes, evaluate company impact",
        "tasks": [
            "analyze mergers and acquisitions",
            "detect corporate strategy changes",
            "evaluate company impact",
        ],
    },
    "health": {
        "model_id": "microsoft/BioGPT-Large",
        "model_type": "local_pipeline",
        "pipeline_task": "text-generation",
        "description": "Interpret scientific/medical news, summarize clinical research, detect public health risk",
        "tasks": [
            "interpret scientific and medical news",
            "summarize clinical research",
            "detect public health risk",
        ],
    },
    "general": {
        "model_id": "meta-llama/Llama-3-8B-Instruct",
        "model_type": "hf_api",
        "description": "Summarize global events, detect disaster impact, provide general reasoning",
        "tasks": [
            "summarize global events",
            "detect disaster impact",
            "provide general reasoning",
        ],
    },
}

# ── Loaded model cache ───────────────────────────────────────────────────────
_loaded_models: Dict[str, Any] = {}


def _truncate(text: str, max_len: int) -> str:
    """Pyre-safe string truncation."""
    if len(text) <= max_len:
        return text
    result: List[str] = []
    i: int = 0
    while i < max_len:
        result.append(text[i])
        i = i + 1
    return "".join(result)


def _first_n_list(items: List[Any], n: int) -> List[Any]:
    """Pyre-safe list slicing."""
    result: List[Any] = []
    count: int = len(items)
    if n < count:
        count = n
    i: int = 0
    while i < count:
        result.append(items[i])
        i = i + 1
    return result


def _round_val(value: float, decimals: int) -> float:
    """Pyre-safe round helper."""
    factor: int = 10 ** decimals
    return float(int(value * factor + 0.5)) / float(factor)


def _get_local_model(sector: str) -> Any:
    """Load a local HuggingFace pipeline model (FinBERT, BioGPT, etc.)."""
    global _loaded_models
    if sector in _loaded_models:
        return _loaded_models[sector]

    model_info: Optional[Dict[str, Any]] = MODEL_REGISTRY.get(sector)
    if model_info is None:
        return None
    if str(model_info.get("model_type", "")) != "local_pipeline":
        return None

    try:
        from transformers import pipeline as hf_pipeline  # type: ignore

        model_id: str = str(model_info["model_id"])
        task: str = str(model_info.get("pipeline_task", "text-generation"))

        logger.info("Loading local model: %s (task: %s)...", model_id, task)
        model = hf_pipeline(task, model=model_id, device=-1)  # type: ignore
        _loaded_models[sector] = model
        logger.info("Model loaded successfully: %s", model_id)
        return model
    except Exception as e:
        logger.warning("Failed to load local model for sector '%s': %s", sector, e)
        return None


def _call_hf_api(model_id: str, prompt: str, max_tokens: int = 256) -> Optional[str]:
    """Call Hugging Face Inference API for large models."""
    if not HF_API_TOKEN:
        logger.debug("No HF_API_TOKEN set, skipping HF API call for %s", model_id)
        return None

    try:
        import requests  # type: ignore

        api_url: str = "https://api-inference.huggingface.co/models/" + model_id
        headers: Dict[str, str] = {"Authorization": "Bearer " + HF_API_TOKEN}
        payload: Dict[str, Any] = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.3,
                "return_full_text": False,
            },
        }

        response = requests.post(api_url, headers=headers, json=payload, timeout=30)  # type: ignore
        response.raise_for_status()  # type: ignore
        result = response.json()  # type: ignore

        if isinstance(result, list) and len(result) > 0:
            first_item: Any = result[0]
            if isinstance(first_item, dict):
                generated: str = str(first_item.get("generated_text", ""))
                return generated.strip() if generated else None
        return None
    except Exception as e:
        logger.warning("HF API call failed for %s: %s", model_id, e)
        return None


# ── Rule-Based Fallback Analyzers ────────────────────────────────────────────

def _count_keywords(text_lower: str, keywords: List[str]) -> int:
    """Count how many keywords appear in text."""
    found: List[str] = []
    for kw in keywords:
        if kw in text_lower:
            found.append(kw)
    return len(found)


def _fallback_finance(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based financial analysis fallback."""
    text_lower: str = text.lower()

    bullish_kw: List[str] = ["surge", "growth", "profit", "rally", "gain", "bullish", "upbeat", "recovery", "boom", "record high"]
    bearish_kw: List[str] = ["crash", "decline", "loss", "recession", "downturn", "bearish", "plunge", "slump", "crisis", "default"]

    bull_count: int = _count_keywords(text_lower, bullish_kw)
    bear_count: int = _count_keywords(text_lower, bearish_kw)

    market_impact: str = "Neutral — mixed market signals"
    if bull_count > bear_count:
        market_impact = "Bullish — positive market signal"
    elif bear_count > bull_count:
        market_impact = "Bearish — negative market signal"

    compound: float = 0.0
    try:
        compound = float(sentiment.get("compound", 0))
    except Exception:
        compound = 0.0

    fin_sentiment: str = "neutral"
    if compound > 0.05:
        fin_sentiment = "positive"
    elif compound < -0.05:
        fin_sentiment = "negative"

    return {
        "model_used": "rule-based (FinBERT fallback)",
        "financial_sentiment": fin_sentiment,
        "market_impact": market_impact,
        "bullish_signals": bull_count,
        "bearish_signals": bear_count,
        "analysis": "Financial sentiment: " + fin_sentiment + ". " + market_impact + ".",
    }


def _fallback_technology(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based technology analysis fallback."""
    text_lower: str = text.lower()

    innovation_kw: List[str] = ["breakthrough", "launch", "release", "innovation", "patent", "discover",
                                "new feature", "upgrade", "next-gen", "revolutionary"]
    risk_kw: List[str] = ["vulnerability", "hack", "breach", "outage", "bug", "failure", "privacy",
                          "regulation", "antitrust", "lawsuit"]

    innovation_count: int = _count_keywords(text_lower, innovation_kw)
    risk_count: int = _count_keywords(text_lower, risk_kw)

    trend: str = "Balanced"
    if innovation_count > risk_count:
        trend = "Innovation-driven"
    elif risk_count > innovation_count:
        trend = "Risk-aware"

    return {
        "model_used": "rule-based (Qwen2 fallback)",
        "trend_type": trend,
        "innovation_signals": innovation_count,
        "risk_signals": risk_count,
        "analysis": "Technology trend: " + trend + ". Innovation signals: " + str(innovation_count) + ", Risk indicators: " + str(risk_count) + ".",
    }


def _fallback_politics(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based political analysis fallback."""
    text_lower: str = text.lower()

    escalation_kw: List[str] = ["war", "conflict", "sanction", "missile", "military", "threat",
                                "invasion", "nuclear", "attack", "tension"]
    stability_kw: List[str] = ["peace", "negotiate", "agreement", "treaty", "cooperation",
                               "alliance", "diplomacy", "ceasefire", "dialogue", "summit"]

    esc_count: int = _count_keywords(text_lower, escalation_kw)
    stab_count: int = _count_keywords(text_lower, stability_kw)

    geo_risk: str = "Low"
    if esc_count >= 3:
        geo_risk = "High"
    elif esc_count >= 1:
        geo_risk = "Moderate"

    return {
        "model_used": "rule-based (Mistral fallback)",
        "geopolitical_risk": geo_risk,
        "escalation_signals": esc_count,
        "stability_signals": stab_count,
        "analysis": "Geopolitical risk: " + geo_risk + ". Escalation: " + str(esc_count) + ", Stability: " + str(stab_count) + ".",
    }


def _fallback_business(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based corporate analysis fallback."""
    text_lower: str = text.lower()

    growth_kw: List[str] = ["merger", "acquisition", "expansion", "growth", "hire", "partnership",
                            "revenue growth", "market share", "invest", "ipo"]
    decline_kw: List[str] = ["layoff", "restructure", "bankruptcy", "shutdown", "loss", "decline",
                             "downsize", "scandal", "investigation", "fine"]

    growth_count: int = _count_keywords(text_lower, growth_kw)
    decline_count: int = _count_keywords(text_lower, decline_kw)

    outlook: str = "Neutral"
    if growth_count > decline_count:
        outlook = "Positive"
    elif decline_count > growth_count:
        outlook = "Negative"

    return {
        "model_used": "rule-based (DeepSeek fallback)",
        "corporate_outlook": outlook,
        "growth_signals": growth_count,
        "decline_signals": decline_count,
        "analysis": "Corporate outlook: " + outlook + ". Growth: " + str(growth_count) + ", Decline: " + str(decline_count) + ".",
    }


def _fallback_health(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based health analysis fallback."""
    text_lower: str = text.lower()

    positive_kw: List[str] = ["cure", "breakthrough", "treatment", "recovery", "vaccine", "approved",
                              "effective", "trial success", "remission", "innovation"]
    risk_kw: List[str] = ["outbreak", "pandemic", "epidemic", "death", "mortality", "side effect",
                          "recall", "warning", "contamination", "mutation"]

    pos_count: int = _count_keywords(text_lower, positive_kw)
    risk_count: int = _count_keywords(text_lower, risk_kw)

    health_risk: str = "Low"
    if risk_count >= 3:
        health_risk = "High"
    elif risk_count >= 1:
        health_risk = "Moderate"

    return {
        "model_used": "rule-based (BioGPT fallback)",
        "public_health_risk": health_risk,
        "positive_signals": pos_count,
        "risk_signals": risk_count,
        "analysis": "Public health risk: " + health_risk + ". Positive: " + str(pos_count) + ", Risk: " + str(risk_count) + ".",
    }


def _fallback_general(text: str, sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based general analysis fallback."""
    text_lower: str = text.lower()

    impact_kw: List[str] = ["disaster", "earthquake", "flood", "hurricane", "wildfire", "tsunami",
                            "crisis", "emergency", "casualty", "evacuation"]
    positive_kw: List[str] = ["celebration", "achievement", "record", "success", "milestone",
                              "award", "victory", "breakthrough", "discovery", "festival"]

    impact_count: int = _count_keywords(text_lower, impact_kw)
    positive_count: int = _count_keywords(text_lower, positive_kw)

    event_type: str = "General News"
    if impact_count >= 2:
        event_type = "Crisis/Disaster"
    elif positive_count >= 2:
        event_type = "Positive Event"

    return {
        "model_used": "rule-based (Llama-3 fallback)",
        "event_type": event_type,
        "impact_signals": impact_count,
        "positive_signals": positive_count,
        "analysis": "Event type: " + event_type + ". Impact: " + str(impact_count) + ", Positive: " + str(positive_count) + ".",
    }


# Fallback function map
_FALLBACK_MAP: Dict[str, Any] = {
    "finance": _fallback_finance,
    "technology": _fallback_technology,
    "politics": _fallback_politics,
    "business": _fallback_business,
    "health": _fallback_health,
    "general": _fallback_general,
}


# ── Core Model Router ────────────────────────────────────────────────────────

def analyze_with_model(
    text: str,
    sector: str,
    sentiment: Dict[str, Any],
    title: str = "",
) -> Dict[str, Any]:
    """
    Route text to the appropriate sector-specific model for deep analysis.
    """
    model_info: Dict[str, Any] = MODEL_REGISTRY.get(sector, MODEL_REGISTRY["general"])
    model_id: str = str(model_info["model_id"])
    model_type: str = str(model_info["model_type"])

    result: Optional[Dict[str, Any]] = None

    # ── 1. Try Local Pipeline (FinBERT, BioGPT) ─────────────────────────────
    if model_type == "local_pipeline":
        model = _get_local_model(sector)
        if model is not None:
            try:
                short_text: str = _truncate(text, 512) if text else "Neutral text"

                if sector == "finance":
                    pred = model(short_text)[0]  # type: ignore
                    label: str = str(pred.get("label", "neutral"))  # type: ignore
                    score: float = float(pred.get("score", 0.0))  # type: ignore
                    result = {
                        "model_used": model_id,
                        "financial_sentiment": label,
                        "confidence": _round_val(score, 4),
                        "analysis": "FinBERT financial sentiment: " + label + " (confidence: " + str(_round_val(score * 100, 1)) + "%)",
                    }
                elif sector == "health":
                    prompt: str = "Medical news analysis: " + _truncate(short_text, 256)
                    gen = model(prompt, max_length=100, num_return_sequences=1)  # type: ignore
                    generated_text: str = ""
                    if gen and isinstance(gen, list) and len(gen) > 0:
                        first: Any = gen[0]
                        if isinstance(first, dict):
                            generated_text = str(first.get("generated_text", ""))
                    result = {
                        "model_used": model_id,
                        "analysis": _truncate(generated_text, 500),
                    }
            except Exception as e:
                logger.warning("Local model failed for sector '%s': %s", sector, e)

    # ── 2. Try HF Inference API (large models) ──────────────────────────────
    if result is None and model_type == "hf_api":
        api_prompt: str = _build_sector_prompt(text, sector, title)
        api_response: Optional[str] = _call_hf_api(model_id, api_prompt)
        if api_response is not None:
            result = {
                "model_used": model_id,
                "analysis": _truncate(api_response, 1000),
            }

    # ── 3. Fallback to rule-based analysis ───────────────────────────────────
    if result is None:
        fallback_fn = _FALLBACK_MAP.get(sector, _fallback_general)
        result = fallback_fn(text, sentiment)

    # Ensure standard fields — result is guaranteed non-None at this point
    final_result: Dict[str, Any] = {}
    if result is not None:
        for _k, _v in result.items():
            final_result[_k] = _v
    final_result["sector"] = sector
    final_result["target_model"] = model_id

    return final_result


def _build_sector_prompt(text: str, sector: str, title: str = "") -> str:
    """Build a sector-appropriate prompt for LLM analysis."""
    short_text: str = _truncate(text, 800) if text else ""

    if sector == "finance":
        return ("You are a financial analyst. Analyze this news for market impact.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Financial sentiment 2) Market impact 3) Affected sectors")
    elif sector == "technology":
        return ("You are a technology analyst. Analyze this tech news.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Innovation trend 2) Impact on tech companies 3) Future implications")
    elif sector == "politics":
        return ("You are a geopolitical analyst. Analyze this political news.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Geopolitical risk level 2) Affected regions 3) Policy implications")
    elif sector == "business":
        return ("You are a corporate analyst. Analyze this business news.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Corporate impact 2) Market strategy 3) Competitive implications")
    elif sector == "health":
        return ("You are a medical research analyst. Analyze this health news.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Public health impact 2) Medical significance 3) Risk assessment")
    else:
        return ("You are a global intelligence analyst. Analyze this news event.\n"
                "Title: " + title + "\nContent: " + short_text + "\n\n"
                "Provide: 1) Event summary 2) Global impact 3) Risk assessment")


def route_and_analyze(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Route each article to its sector-specific model and perform deep analysis.
    Adds 'model_analysis' field to each article.
    """
    sector_counts: Dict[str, int] = {}
    model_counts: Dict[str, int] = {}

    for article in articles:
        sector: str = str(article.get("sector", "general"))
        sentiment: Dict[str, Any] = article.get("sentiment", {"label": "Neutral", "compound": 0.0})
        if not isinstance(sentiment, dict):
            sentiment = {"label": "Neutral", "compound": 0.0}
        text: str = str(article.get(
            "clean_text",
            str(article.get("title", "")) + " " + str(article.get("description", "")),
        ))
        title: str = str(article.get("title", ""))

        analysis: Dict[str, Any] = analyze_with_model(text, sector, sentiment, title)
        article["model_analysis"] = analysis

        # Track stats
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
        model_used: str = str(analysis.get("model_used", "unknown"))
        model_counts[model_used] = model_counts.get(model_used, 0) + 1

    # Log routing statistics
    logger.info(
        "Model routing complete: %d articles processed across %d sectors",
        len(articles),
        len(sector_counts),
    )
    for model, count in sorted(model_counts.items(), key=lambda x: -x[1]):
        logger.info("  → %s: %d articles", model, count)

    return articles


def generate_intelligence_output(
    event: Dict[str, Any],
    articles: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate the final intelligence output for an event.
    """
    # Gather articles for this event
    raw_indices: Any = event.get("article_indices", [])
    if not isinstance(raw_indices, list):
        raw_indices = []

    event_articles: List[Dict[str, Any]] = []
    j: int = 0
    while j < len(raw_indices):
        idx_val: Any = raw_indices[j]
        if isinstance(idx_val, int) and idx_val < len(articles):
            event_articles.append(articles[idx_val])
        j = j + 1

    if len(event_articles) == 0:
        return {
            "event_title": str(event.get("label", "Unknown Event")),
            "sector": "general",
            "summary": str(event.get("ai_summary", "")),
            "sentiment": "Neutral",
            "importance_score": 0,
            "risk_score": 0,
            "impacted_sectors": [],
        }

    # Determine primary sector (most common among event articles)
    sector_votes: Dict[str, int] = {}
    for a in event_articles:
        s: str = str(a.get("sector", "general"))
        sector_votes[s] = sector_votes.get(s, 0) + 1

    primary_sector: str = "general"
    max_votes: int = 0
    for s_key, s_count in sector_votes.items():
        if s_count > max_votes:
            max_votes = s_count
            primary_sector = s_key

    # Aggregate sentiment
    compound_values: List[float] = []
    for a in event_articles:
        sent: Any = a.get("sentiment", {})
        if isinstance(sent, dict):
            try:
                c_val: float = float(sent.get("compound", 0.0))
                compound_values.append(c_val)
            except Exception:
                pass

    avg_compound: float = 0.0
    if len(compound_values) > 0:
        total_c: float = sum(compound_values)
        avg_compound = total_c / float(len(compound_values))

    sentiment_label: str = "Neutral"
    if avg_compound >= 0.05:
        sentiment_label = "Positive"
    elif avg_compound <= -0.05:
        sentiment_label = "Negative"

    # Collect impacted sectors
    impacted_set: Dict[str, bool] = {}
    for a in event_articles:
        sec_name: str = str(a.get("sector", "general"))
        if sec_name:
            impacted_set[sec_name] = True
        raw_impacts: Any = a.get("impacts", [])
        if isinstance(raw_impacts, list):
            for impact in raw_impacts:
                if isinstance(impact, dict):
                    imp_sector: str = str(impact.get("sector", ""))
                    if imp_sector:
                        impacted_set[imp_sector] = True

    impacted_list: List[str] = sorted(impacted_set.keys())
    impacted_list = _first_n_list(impacted_list, 10)  # type: ignore

    # Build summary
    summary: str = str(event.get("ai_summary", ""))
    if not summary:
        for a in event_articles:
            ma: Any = a.get("model_analysis", {})
            if isinstance(ma, dict):
                analysis_text: str = str(ma.get("analysis", ""))
                if analysis_text:
                    summary = _truncate(analysis_text, 500)
                    break

    return {
        "event_title": str(event.get("label", "Unknown Event")),
        "sector": primary_sector,
        "summary": summary,
        "sentiment": sentiment_label,
        "importance_score": event.get("importance_score", 0),
        "risk_score": event.get("risk_score", 0),
        "impacted_sectors": impacted_list,
    }


def generate_all_intelligence(
    events: List[Dict[str, Any]],
    articles: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate intelligence output for all events."""
    outputs: List[Dict[str, Any]] = []
    for event in events:
        output: Dict[str, Any] = generate_intelligence_output(event, articles)
        outputs.append(output)

    logger.info("Generated intelligence output for %d events.", len(outputs))
    return outputs


def get_model_info() -> Dict[str, Dict[str, Any]]:
    """Return information about all registered models (for API/dashboard)."""
    info: Dict[str, Dict[str, Any]] = {}
    for sector, model in MODEL_REGISTRY.items():
        model_type: str = str(model.get("model_type", ""))
        hf_available: bool = True
        if model_type == "hf_api":
            hf_available = bool(HF_API_TOKEN)

        info[sector] = {
            "model_id": str(model["model_id"]),
            "model_type": model_type,
            "description": str(model["description"]),
            "tasks": model["tasks"],
            "loaded": sector in _loaded_models,
            "hf_api_available": hf_available,
        }
    return info

"""
VEILORACLE — Sector Router
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Classifies articles into primary sectors using keyword matching.
Routes each article to the correct sector for downstream AI model routing.

Sectors:
  finance  → FinBERT
  technology → Qwen2
  politics → Mistral
  business → DeepSeek
  health   → BioGPT
  general  → Llama 3
"""

import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger("veiloracle.sector_router")

# ── Sector keyword definitions ───────────────────────────────────────────────
# Each sector has weighted keywords: (keyword, weight)
# Higher weight = stronger signal for that sector

SECTOR_KEYWORDS: Dict[str, List[Tuple[str, int]]] = {
    "finance": [
        ("stock", 3), ("market", 2), ("trading", 3), ("investment", 3),
        ("bank", 2), ("bonds", 3), ("interest rate", 3), ("inflation", 3),
        ("gdp", 3), ("economy", 2), ("federal reserve", 3), ("wall street", 3),
        ("nasdaq", 3), ("nyse", 3), ("s&p 500", 3), ("dow jones", 3),
        ("hedge fund", 3), ("mutual fund", 3), ("forex", 3), ("commodity", 2),
        ("bull market", 3), ("bear market", 3), ("ipo", 3), ("dividend", 3),
        ("recession", 3), ("cryptocurrency", 2), ("bitcoin", 2), ("ethereum", 2),
        ("treasury", 2), ("fiscal", 2), ("monetary policy", 3), ("central bank", 3),
        ("credit", 2), ("debt", 2), ("securities", 3), ("portfolio", 2),
        ("earnings", 2), ("revenue", 1), ("profit", 1), ("valuation", 2),
        ("financial", 2), ("fintech", 2), ("insurance", 2), ("mortgage", 2),
    ],
    "technology": [
        ("artificial intelligence", 3), ("ai ", 2), ("machine learning", 3),
        ("deep learning", 3), ("neural network", 3), ("software", 2),
        ("hardware", 2), ("semiconductor", 3), ("chip", 2), ("processor", 2),
        ("quantum computing", 3), ("blockchain", 2), ("cloud computing", 3),
        ("saas", 3), ("cybersecurity", 3), ("data center", 3), ("5g", 3),
        ("startup", 2), ("silicon valley", 3), ("tech giant", 3),
        ("apple", 1), ("google", 1), ("microsoft", 1), ("nvidia", 2),
        ("openai", 3), ("chatgpt", 3), ("large language model", 3), ("llm", 3),
        ("robotics", 2), ("automation", 2), ("internet of things", 3),
        ("virtual reality", 3), ("augmented reality", 3), ("metaverse", 3),
        ("smartphone", 2), ("laptop", 1), ("gadget", 2), ("innovation", 1),
        ("developer", 2), ("programming", 2), ("algorithm", 2), ("api", 2),
        ("autonomous", 2), ("self-driving", 3), ("drone", 2), ("wearable", 2),
    ],
    "politics": [
        ("election", 3), ("president", 2), ("government", 2), ("congress", 3),
        ("parliament", 3), ("senate", 3), ("legislation", 3), ("bill", 1),
        ("vote", 2), ("democrat", 3), ("republican", 3), ("campaign", 2),
        ("diplomat", 3), ("sanction", 3), ("treaty", 3), ("embassy", 3),
        ("geopolitical", 3), ("geopolitics", 3), ("nato", 3), ("united nations", 3),
        ("foreign policy", 3), ("war", 2), ("conflict", 2), ("military", 2),
        ("defense", 2), ("nuclear", 2), ("missile", 3), ("espionage", 3),
        ("political", 2), ("ideology", 2), ("referendum", 3), ("protest", 2),
        ("coup", 3), ("regime", 3), ("sovereignty", 3), ("annexation", 3),
        ("immigration", 2), ("border", 2), ("tariff", 2), ("trade war", 3),
        ("supreme court", 3), ("judiciary", 2), ("constitutional", 2),
        ("prime minister", 3), ("chancellor", 2), ("diplomacy", 3),
    ],
    "business": [
        ("merger", 3), ("acquisition", 3), ("takeover", 3), ("ipo", 2),
        ("corporate", 2), ("ceo", 2), ("executive", 2), ("board of directors", 3),
        ("quarterly report", 3), ("earnings report", 3), ("annual report", 2),
        ("supply chain", 3), ("logistics", 2), ("retail", 2), ("e-commerce", 2),
        ("consumer", 1), ("brand", 1), ("franchise", 2), ("startup", 1),
        ("venture capital", 3), ("private equity", 3), ("restructuring", 3),
        ("bankruptcy", 3), ("layoff", 3), ("hiring", 2), ("workforce", 2),
        ("revenue", 2), ("profit", 2), ("loss", 1), ("quarterly", 2),
        ("shareholder", 3), ("stakeholder", 2), ("dividend", 2),
        ("management", 1), ("strategy", 1), ("operations", 1),
        ("partnership", 2), ("joint venture", 3), ("spin-off", 3),
        ("conglomerate", 3), ("corporation", 2), ("enterprise", 2),
        ("market share", 3), ("competitive", 2), ("disruption", 2),
    ],
    "health": [
        ("vaccine", 3), ("drug", 2), ("pharmaceutical", 3), ("pharma", 3),
        ("clinical trial", 3), ("fda", 3), ("who", 2), ("pandemic", 3),
        ("epidemic", 3), ("virus", 2), ("disease", 2), ("cancer", 3),
        ("treatment", 2), ("therapy", 2), ("hospital", 2), ("surgery", 2),
        ("medical", 2), ("healthcare", 2), ("health care", 2),
        ("biotech", 3), ("biotechnology", 3), ("genomics", 3), ("gene therapy", 3),
        ("mental health", 3), ("diagnosis", 2), ("patient", 2),
        ("public health", 3), ("cdc", 3), ("nih", 3), ("research", 1),
        ("clinical", 2), ("biomedical", 3), ("pathogen", 3), ("antibody", 3),
        ("immunology", 3), ("oncology", 3), ("neuroscience", 3),
        ("alzheimer", 3), ("diabetes", 3), ("obesity", 2), ("nutrition", 2),
        ("wellness", 1), ("medicare", 3), ("medicaid", 3), ("insurance", 1),
    ],
}

# Minimum score threshold for sector classification
MIN_SECTOR_SCORE = 3


def _round_val(value: float, decimals: int) -> float:
    """Pyre-safe rounding helper."""
    factor = 10 ** decimals
    return float(int(value * factor + 0.5)) / float(factor)


def classify_sector(text: str) -> Dict[str, Any]:
    """
    Classify text into a primary sector with confidence score.
    Returns: {sector, confidence, scores, matched_keywords}
    """
    if not text:
        return {"sector": "general", "confidence": 0.0, "scores": {}, "matched_keywords": []}

    text_lower = text.lower()
    scores: Dict[str, float] = {}
    matched: Dict[str, List[str]] = {}

    for sector, keywords in SECTOR_KEYWORDS.items():
        weight_list: List[float] = []
        sector_matches: List[str] = []
        for keyword, weight in keywords:
            if keyword in text_lower:
                weight_list.append(float(weight))
                sector_matches.append(keyword)
        scores[sector] = sum(weight_list)
        matched[sector] = sector_matches

    # Find the best sector
    best_sector: str = "general"
    best_score: float = 0.0
    for k, v in scores.items():
        if v > best_score:
            best_score = v
            best_sector = k

    # Fall back to "general" if score is too low
    if best_score < MIN_SECTOR_SCORE:
        best_sector = "general"

    # Normalize confidence (0.0 to 1.0)
    sector_kw_list = SECTOR_KEYWORDS.get(best_sector, [])
    max_possible: float = 0.0
    for _kw, w in sector_kw_list:
        max_possible = max_possible + float(w)
    if max_possible < 1.0:
        max_possible = 1.0

    confidence = best_score / (max_possible * 0.3)
    if confidence > 1.0:
        confidence = 1.0

    rounded_scores: Dict[str, float] = {}
    for k, v in scores.items():
        rounded_scores[k] = _round_val(v, 2)

    return {
        "sector": best_sector,
        "confidence": _round_val(confidence, 4),
        "scores": rounded_scores,
        "matched_keywords": matched.get(best_sector, []),
    }


def route_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classify each article into a sector and add sector routing info.
    Adds 'sector', 'sector_confidence', and 'sector_keywords' fields.
    """
    sector_counts: Dict[str, int] = {}

    for article in articles:
        text: str = article.get(
            "clean_text",
            str(article.get("title", "")) + " " + str(article.get("description", ""))
        )
        result = classify_sector(text)

        article["sector"] = result["sector"]
        article["sector_confidence"] = result["confidence"]
        article["sector_keywords"] = result["matched_keywords"]

        sec: str = str(result["sector"])
        sector_counts[sec] = sector_counts.get(sec, 0) + 1

    # Log distribution
    dist_parts: List[str] = []
    for k, v in sorted(sector_counts.items(), key=lambda x: -x[1]):
        dist_parts.append(str(k) + ": " + str(v))
    dist_str = ", ".join(dist_parts)
    logger.info("Sector routing: %d articles → %s", len(articles), dist_str)

    return articles


def get_sector_distribution(articles: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get article count per sector."""
    dist: Dict[str, int] = {}
    for article in articles:
        sector: str = str(article.get("sector", "general"))
        dist[sector] = dist.get(sector, 0) + 1
    return dist


def get_articles_by_sector(
    articles: List[Dict[str, Any]], sector: str
) -> List[Dict[str, Any]]:
    """Filter articles by sector."""
    result: List[Dict[str, Any]] = []
    for a in articles:
        if a.get("sector") == sector:
            result.append(a)
    return result

"""
VEILORACLE — Named Entity Recognition Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uses spaCy NLP to extract entities: people, organizations, locations, money, dates.
Falls back to regex-based extraction if spaCy is unavailable.
"""

import logging
import re
from collections import Counter

logger = logging.getLogger("veiloracle.ner")

_nlp = None
_use_spacy = True


def _get_nlp():
    global _nlp, _use_spacy
    if _nlp is None:
        try:
            import spacy  # type: ignore
            try:
                _nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.info("Downloading spaCy en_core_web_sm model...")
                from spacy.cli import download  # type: ignore
                download("en_core_web_sm")
                _nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy NER model loaded.")
        except Exception as e:
            logger.warning("spaCy not available (%s), using regex fallback.", e)
            _use_spacy = False
            _nlp = "fallback"
    return _nlp


# Predefined named entities for regex fallback when spaCy is not available
KNOWN_ORGS = [
    "Google", "Apple", "Microsoft", "Amazon", "Tesla", "Meta", "Netflix",
    "NVIDIA", "Intel", "AMD", "Samsung", "IBM", "Oracle", "Cisco", "Adobe",
    "Salesforce", "SpaceX", "Boeing", "Airbus", "Toyota", "Ford", "BMW",
    "JPMorgan", "Goldman Sachs", "Morgan Stanley", "BlackRock", "Berkshire",
    "Federal Reserve", "NYSE", "NASDAQ", "SEC", "FDA", "WHO", "NATO", "UN",
    "Reuters", "Bloomberg", "BBC", "CNN", "CNBC", "TechCrunch", "Wired"
]

KNOWN_PEOPLE = [
    "Elon Musk", "Tim Cook", "Satya Nadella", "Mark Zuckerberg", "Jeff Bezos",
    "Jensen Huang", "Sam Altman", "Sundar Pichai", "Warren Buffett", "Jamie Dimon",
    "Jerome Powell", "Janet Yellen", "Christine Lagarde"
]

KNOWN_LOCATIONS = [
    "United States", "China", "India", "Europe", "Japan", "UK", "Germany",
    "Silicon Valley", "Wall Street", "Washington", "Beijing", "Tokyo",
    "London", "New York", "San Francisco", "Shanghai"
]


def _regex_extract(text: str) -> list[dict]:
    """Regex-based entity extraction fallback."""
    entities = []
    text_lower = text.lower()

    for org in KNOWN_ORGS:
        if org.lower() in text_lower:
            entities.append({"text": org, "label": "ORG", "count": text_lower.count(org.lower())})

    for person in KNOWN_PEOPLE:
        if person.lower() in text_lower:
            entities.append({"text": person, "label": "PERSON", "count": text_lower.count(person.lower())})

    for loc in KNOWN_LOCATIONS:
        if loc.lower() in text_lower:
            entities.append({"text": loc, "label": "GPE", "count": text_lower.count(loc.lower())})

    # Detect money amounts
    money_pattern = r'\$[\d,]+(?:\.\d{1,2})?(?:\s*(?:billion|million|trillion))?'
    for match in re.finditer(money_pattern, text, re.IGNORECASE):
        entities.append({"text": match.group(), "label": "MONEY", "count": 1})

    return entities


def extract_entities(text: str) -> list[dict]:
    """Extract named entities from text. Returns list of {text, label, count}."""
    if not text:
        return []

    nlp = _get_nlp()

    if _use_spacy and nlp != "fallback":
        try:
            doc = nlp(text[:5000])  # type: ignore
            entity_counts = Counter()
            entity_labels = {}
            for ent in doc.ents:
                if ent.label_ in ("PERSON", "ORG", "GPE", "LOC", "MONEY", "DATE", "NORP", "EVENT"):
                    clean = ent.text.strip()
                    if len(clean) > 1:
                        entity_counts[clean] += 1
                        entity_labels[clean] = ent.label_
            return [{"text": text, "label": entity_labels[text], "count": count}
                    for text, count in entity_counts.most_common(20)]
        except Exception as e:
            logger.warning("spaCy extraction failed: %s, using regex", e)
            return _regex_extract(text)
    else:
        return _regex_extract(text)


def extract_from_articles(articles: list[dict]) -> dict:
    """Extract entities from all articles, returning aggregated counts."""
    all_entities = Counter()
    entity_labels = {}

    for article in articles:
        text = article.get("clean_text", f"{article.get('title', '')} {article.get('description', '')}")
        entities = extract_entities(text)
        for ent in entities:
            key = ent["text"]
            all_entities[key] += ent["count"]
            entity_labels[key] = ent["label"]

    top_entities = [
        {"text": text, "label": entity_labels[text], "count": count}
        for text, count in all_entities.most_common(50)
    ]

    # Group by category
    grouped = {
        "PERSON": [e for e in top_entities if e["label"] == "PERSON"],
        "ORG": [e for e in top_entities if e["label"] == "ORG"],
        "GPE": [e for e in top_entities if e["label"] in ("GPE", "LOC")],
        "MONEY": [e for e in top_entities if e["label"] == "MONEY"],
        "OTHER": [e for e in top_entities if e["label"] not in ("PERSON", "ORG", "GPE", "LOC", "MONEY")]
    }

    logger.info("NER: extracted %d unique entities from %d articles", len(top_entities), len(articles))
    return {"entities": top_entities, "grouped": grouped}


def enrich_articles_with_entities(articles: list[dict]) -> list[dict]:
    """Add 'entities' field to each article."""
    for article in articles:
        text = article.get("clean_text", f"{article.get('title', '')} {article.get('description', '')}")
        article["entities"] = extract_entities(text)
    logger.info("Enriched %d articles with NER entities.", len(articles))
    return articles

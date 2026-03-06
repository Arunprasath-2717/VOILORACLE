"""
VEILORACLE — Topic Discovery Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Automatically detects new news topics using BERTopic.
"""

import logging

logger = logging.getLogger("veiloracle.topic")

_topic_model = None

def _get_topic_model():
    global _topic_model
    if _topic_model is None:
        try:
            from bertopic import BERTopic
            from sentence_transformers import SentenceTransformer
            from backend import config
            
            logger.info("Loading BERTopic...")
            embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
            # Use English by default, mapping to mini LM or configured BGE small
            _topic_model = BERTopic(embedding_model=embedding_model, min_topic_size=2)
        except Exception as e:
            logger.warning("BERTopic not available: %s", e)
            _topic_model = "fallback"
    return _topic_model

def discover_topics(articles: list[dict]) -> dict:
    model = _get_topic_model()
    if model == "fallback" or not articles:
        return {"topics": []}
        
    texts = [a.get("clean_text", f"{a.get('title','')} {a.get('description','')}") for a in articles]
    if len(texts) < 3:
        return {"topics": []}
        
    try:
        topics, probs = model.fit_transform(texts)
        topic_info = model.get_topic_info()
        found_topics = []
        for idx, row in topic_info.iterrows():
            if row['Topic'] != -1:
                topic_words = model.get_topic(row['Topic'])
                words = [w[0] for w in topic_words[:5]]
                found_topics.append({
                    "topic_id": int(row['Topic']),
                    "name": row['Name'],
                    "count": int(row['Count']),
                    "keywords": words
                })
        return {"topics": found_topics}
    except Exception as e:
        logger.error("Topic discovery failed: %s", e)
        return {"topics": []}

"""
VEILORACLE — Event Detector
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groups articles into events via sentence embeddings + DBSCAN.
"""

import logging
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances

from backend import config
from backend import gemini_engine

logger = logging.getLogger("veiloracle.detector")

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading embedding model: %s", config.EMBEDDING_MODEL)
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def generate_embeddings(texts: list[str]) -> np.ndarray:
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    logger.info("Embeddings: shape %s", embeddings.shape)
    return embeddings


def cluster_articles(embeddings: np.ndarray) -> np.ndarray:
    if len(embeddings) < 2:
        return np.array([-1] * len(embeddings))
    distance_matrix = cosine_distances(embeddings)
    labels = DBSCAN(eps=config.DBSCAN_EPS, min_samples=config.DBSCAN_MIN_SAMPLES,
                    metric="precomputed").fit(distance_matrix).labels_
    logger.info("DBSCAN: %d clusters, %d noise", len(set(labels) - {-1}), (labels == -1).sum())
    return labels


def _find_representative(indices: list[int], embeddings: np.ndarray) -> int:
    cluster_emb = embeddings[indices]
    centroid = cluster_emb.mean(axis=0)
    return indices[int(np.argmin(np.linalg.norm(cluster_emb - centroid, axis=1)))]


def detect_events(articles: list[dict]) -> list[dict]:
    """Full event detection: embed → cluster → extract."""
    if not articles:
        return []
    texts = [a.get("clean_text", f"{a.get('title','')} {a.get('description','')}") for a in articles]
    embeddings = generate_embeddings(texts)
    labels = cluster_articles(embeddings)

    events = []
    for label_id in sorted(set(labels)):
        if label_id == -1:
            for idx in [i for i, l in enumerate(labels) if l == -1]:
                events.append({"event_id": f"standalone_{idx}", "label": articles[idx].get("title", ""),
                               "article_indices": [idx], "size": 1, "representative_idx": idx, "is_cluster": False})
            continue
        
        indices = [i for i, l in enumerate(labels) if l == label_id]
        rep = _find_representative(indices, embeddings)
        
        # Use representative article title as label (skip Gemini to preserve API quota)
        label = articles[rep].get("title", f"Event {label_id}")
                
        events.append({"event_id": f"cluster_{label_id}", "label": label,
                       "article_indices": indices, "size": len(indices), "representative_idx": rep, "is_cluster": True})

    events.sort(key=lambda e: (-int(e["is_cluster"]), -e["size"]))
    logger.info("Detected %d events (%d clusters, %d standalone)", len(events),
                sum(1 for e in events if e["is_cluster"]), sum(1 for e in events if not e["is_cluster"]))
    return events

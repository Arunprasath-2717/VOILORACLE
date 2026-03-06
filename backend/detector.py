"""
VEILORACLE — Event Detector
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Groups articles into events via sentence embeddings + HDBSCAN.
Includes deduplication, source credibility, time decay, and lifecycle tracking.
"""

import logging
from typing import Any, List, Dict, Set
import numpy as np  # type: ignore
import hdbscan  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances  # type: ignore
from datetime import datetime

from backend import config  # type: ignore

logger = logging.getLogger("veiloracle.detector")

_model = None

def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # type: ignore
        logger.info("Loading embedding model: %s", config.EMBEDDING_MODEL)
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model

def generate_embeddings(texts: list[str]) -> np.ndarray:
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    logger.info("Embeddings: shape %s", embeddings.shape)
    return embeddings

def detect_duplicates(articles: List[Dict[str, Any]], embeddings: Any) -> List[int]:
    """Flag duplicate articles using cosine similarity > 0.95"""
    sim_matrix = cosine_similarity(embeddings)
    duplicates: Set[int] = set()
    for i in range(len(articles)):
        if i in duplicates:
            continue
        for j in range(i + 1, len(articles)):
            if sim_matrix[i, j] > 0.95:  # type: ignore
                duplicates.add(j)
    return list(duplicates)

def _get_credibility(source: str) -> float:
    if not source: return config.DEFAULT_CREDIBILITY
    source_lower = source.lower()
    for key, val in config.SOURCE_CREDIBILITY.items():
        if key in source_lower:
            return val
    return config.DEFAULT_CREDIBILITY

def _calculate_weights(articles: list[dict]) -> np.ndarray:
    now = datetime.utcnow()
    weights = []
    
    for a in articles:
        # Time decay
        pub_str = a.get("published_at")
        hours_diff = 0
        if pub_str:
            try:
                # Naive parse, assumes ISO format
                pub = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
                dt = (now - pub.replace(tzinfo=None)).total_seconds() / 3600
                hours_diff = float(max(0.0, dt))
            except:
                pass
        decay_weight = np.exp(-0.05 * hours_diff) # Half-life ~14 hours
        
        # Credibility
        cred_weight = _get_credibility(a.get("source", ""))
        
        weights.append(decay_weight * cred_weight)
    
    return np.array(weights)

def cluster_articles(embeddings: np.ndarray) -> np.ndarray:
    if len(embeddings) < 2:
        return np.array([-1] * len(embeddings))
    distance_matrix = cosine_distances(embeddings)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=config.HDBSCAN_MIN_CLUSTER_SIZE,
        min_samples=config.HDBSCAN_MIN_SAMPLES,
        metric="precomputed"
    )
    labels = clusterer.fit_predict(distance_matrix.astype(np.float64))
    noise_count = int(sum(1 for x in labels if x == -1))
    logger.info("HDBSCAN: %d clusters, %d noise", len(set(labels) - {-1}), noise_count)
    return labels

def _find_representative(indices: list[int], embeddings: np.ndarray) -> int:
    cluster_emb = embeddings[indices]
    centroid = cluster_emb.mean(axis=0)
    return indices[int(np.argmin(np.linalg.norm(cluster_emb - centroid, axis=1)))]

def _determine_lifecycle(cluster_size: int, avg_age_hours: float) -> str:
    """Classify event lifecycle."""
    if cluster_size > 10 and avg_age_hours < 24:
        return "trending"
    elif cluster_size > 20 and avg_age_hours >= 24:
        return "peak"
    elif cluster_size <= 10 and avg_age_hours < 12:
        return "emerging"
    else:
        return "declining"

def detect_events(articles: list[dict]) -> list[dict]:
    """Full event detection: deduplicate → embed → cluster → extract → lifecycle."""
    if not articles:
        return []
        
    texts = [a.get("clean_text", f"{a.get('title','')} {a.get('description','')}") for a in articles]
    all_embeddings = generate_embeddings(texts)
    
    # 1. Deduplicate
    duplicates = detect_duplicates(articles, all_embeddings)
    logger.info(f"Removed {len(duplicates)} duplicates based on similarity > 0.95")
    
    valid_indices = [i for i in range(len(articles)) if i not in duplicates]
    if not valid_indices:
        articles.clear()
        return []
        
    embeddings = all_embeddings[valid_indices]
    
    # Store embeddings and update articles in-place to remove docs
    for i, orig_idx in enumerate(valid_indices):
        articles[orig_idx]["embedding"] = all_embeddings[orig_idx].tolist()  # type: ignore
        
    updated = [articles[i] for i in valid_indices]
    articles.clear()
    articles.extend(updated)
    
    # 2. Cluster
    labels = cluster_articles(embeddings)
    weights = _calculate_weights(articles)
    now = datetime.utcnow()

    events = []
    for label_id in sorted(set(labels)):
        cluster_valid_idx = [i for i, l in enumerate(labels) if l == label_id]
        
        if label_id == -1:
            for i in cluster_valid_idx:
                events.append({
                    "event_id": f"standalone_{i}", 
                    "label": articles[i].get("title", ""),
                    "article_indices": [i], 
                    "size": 1, 
                    "weight_score": round(float(weights[i]), 4),  # type: ignore
                    "representative_idx": i, 
                    "is_cluster": False,
                    "lifecycle": "emerging"
                })
            continue
            
        rep_orig_idx = cluster_valid_idx[_find_representative(cluster_valid_idx, embeddings)]
        label = articles[rep_orig_idx].get("title", f"Event {label_id}")
        
        # Calculate cluster weight & lifecycle
        cluster_weight = float(np.sum(weights[cluster_valid_idx]))
        
        ages_hours = []
        for orig_idx in cluster_valid_idx:
            pub_str = str(articles[orig_idx].get("published_at", ""))
            if pub_str:
                try:
                    pub = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
                    dt = (now - pub.replace(tzinfo=None)).total_seconds() / 3600
                    ages_hours.append(float(max(0.0, dt)))
                except:
                    ages_hours.append(12.0)
            else:
                ages_hours.append(12.0)
                
        avg_age = sum(ages_hours) / len(ages_hours) if ages_hours else 12
        lifecycle = _determine_lifecycle(len(cluster_valid_idx), avg_age)
                
        events.append({
            "event_id": f"cluster_{label_id}", 
            "label": label,
            "article_indices": cluster_valid_idx, 
            "size": len(cluster_valid_idx), 
            "weight_score": round(cluster_weight, 4),  # type: ignore
            "representative_idx": rep_orig_idx, 
            "is_cluster": True,
            "lifecycle": lifecycle
        })

    events.sort(key=lambda e: (-e["weight_score"], -int(e["is_cluster"])))
    logger.info("Detected %d events (%d clusters, %d standalone)", len(events),
                sum(1 for e in events if e["is_cluster"]), sum(1 for e in events if not e["is_cluster"]))
    return events

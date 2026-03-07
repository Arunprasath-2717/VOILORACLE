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
    """Load the sentence transformer model globally."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # type: ignore
        logger.info("Loading embedding model: %s", config.EMBEDDING_MODEL)
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def generate_embeddings(texts: list[str]) -> np.ndarray:
    """Generate embeddings for a list of text strings."""
    if not texts:
        return np.array([])
    
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    logger.info("Generated embeddings: shape %s", embeddings.shape)
    return embeddings


def detect_duplicates(articles: List[Dict[str, Any]], embeddings: np.ndarray) -> List[int]:
    """
    Flag duplicate articles using cosine similarity > 0.95.
    Returns list of indices to remove.
    """
    if len(articles) < 2 or len(embeddings) < 2:
        return []
    
    sim_matrix = cosine_similarity(embeddings)
    duplicates: Set[int] = set()
    
    for i in range(len(articles)):
        if i in duplicates:
            continue
        for j in range(i + 1, len(articles)):
            if sim_matrix[i, j] > 0.95:  # type: ignore
                duplicates.add(j)
    
    return sorted(list(duplicates), reverse=True)


def _get_credibility(source: str) -> float:
    """Get source credibility from config, default if unknown."""
    if not source:
        return config.DEFAULT_CREDIBILITY
    
    source_lower = source.lower()
    for key, val in config.SOURCE_CREDIBILITY.items():
        if key.lower() in source_lower:
            return val
    
    return config.DEFAULT_CREDIBILITY


def _calculate_weights(articles: list[dict]) -> np.ndarray:
    """Calculate time-decay and credibility-weighted scores."""
    if not articles:
        return np.array([])
    
    now = datetime.utcnow()
    weights = []
    
    for article in articles:
        # Time decay: exponential with lambda=0.05 per hour
        pub_str = article.get("published_at", "")
        hours_diff = 0.0
        
        if pub_str:
            try:
                # Parse ISO format (handles UTC with 'Z' or '+00:00')
                pub = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
                dt = (now - pub.replace(tzinfo=None)).total_seconds() / 3600
                hours_diff = float(max(0.0, dt))
            except Exception as e:
                logger.debug("Failed to parse published_at: %s", e)
                hours_diff = 6.0  # Default to 6 hours if parse fails
        
        decay_weight = np.exp(-0.05 * hours_diff)  # Half-life ~14 hours
        
        # Credibility multiplier
        cred_weight = _get_credibility(article.get("source", ""))
        
        weights.append(decay_weight * cred_weight)
    
    return np.array(weights)


def cluster_articles(embeddings: np.ndarray) -> np.ndarray:
    """
    Cluster articles using HDBSCAN on precomputed cosine distance matrix.
    Returns array of cluster labels (-1 for noise).
    """
    if len(embeddings) < 2:
        return np.array([-1] * len(embeddings))
    
    # Compute cosine distance matrix
    distance_matrix = cosine_distances(embeddings)
    
    # Cluster with HDBSCAN
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=config.HDBSCAN_MIN_CLUSTER_SIZE,
        min_samples=config.HDBSCAN_MIN_SAMPLES,
        metric="precomputed"
    )
    labels = clusterer.fit_predict(distance_matrix.astype(np.float64))
    
    # Log clustering results
    unique_labels = set(labels)
    num_clusters = len(unique_labels - {-1})
    noise_count = int(sum(1 for x in labels if x == -1))
    
    logger.info("HDBSCAN clustering: %d clusters, %d noise points", num_clusters, noise_count)
    
    return labels


def _find_representative(cluster_indices: list[int], embeddings: np.ndarray) -> int:
    """
    Find the representative article for a cluster.
    
    Args:
        cluster_indices: List of article indices in the cluster
        embeddings: Full embedding matrix for all articles
    
    Returns:
        The actual article index of the cluster representative (closest to centroid)
    
    Raises:
        ValueError: If cluster_indices is empty
    """
    if not cluster_indices:
        raise ValueError("Cannot find representative of empty cluster")
    
    # Extract embeddings for this cluster
    cluster_embeddings = embeddings[cluster_indices]
    
    # Compute centroid
    centroid = cluster_embeddings.mean(axis=0)
    
    # Find embedding closest to centroid
    distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
    closest_idx = int(np.argmin(distances))
    
    # Return the actual article index (not the position in cluster_indices)
    return cluster_indices[closest_idx]


def _determine_lifecycle(cluster_size: int, avg_age_hours: float) -> str:
    """Classify event lifecycle based on cluster size and age."""
    if cluster_size > 10 and avg_age_hours < 24:
        return "trending"
    elif cluster_size > 20 and avg_age_hours >= 24:
        return "peak"
    elif cluster_size <= 10 and avg_age_hours < 12:
        return "emerging"
    else:
        return "declining"


def detect_events(articles: list[dict]) -> list[dict]:
    """
    Full event detection pipeline:
    1. Generate embeddings for all articles
    2. Remove duplicates (similarity > 0.95)
    3. Cluster with HDBSCAN
    4. Select representative article for each cluster
    5. Calculate weight scores (time-decay + credibility)
    6. Determine lifecycle stage
    7. Return structured event objects
    
    Args:
        articles: List of article dicts with 'title', 'description', 'published_at', 'source'
    
    Returns:
        List of event dicts with clustering and lifecycle information
    """
    if not articles:
        logger.info("No articles to detect events from")
        return []
    
    logger.info("Starting event detection for %d articles", len(articles))
    
    # Step 1: Generate embeddings
    texts = [
        article.get("clean_text") or 
        f"{article.get('title', '')} {article.get('description', '')}"
        for article in articles
    ]
    
    all_embeddings = generate_embeddings(texts)
    
    if len(all_embeddings) == 0:
        logger.warning("Failed to generate embeddings")
        return []
    
    # Step 2: Detect and remove duplicates
    duplicate_indices = detect_duplicates(articles, all_embeddings)
    
    if duplicate_indices:
        logger.info("Removing %d duplicate articles", len(duplicate_indices))
        for idx in duplicate_indices:
            articles[idx]["_duplicate"] = True
    
    # Filter out duplicates
    valid_indices = [i for i in range(len(articles)) if i not in duplicate_indices]
    
    if not valid_indices:
        logger.warning("All articles are duplicates")
        return []
    
    # Create filtered arrays
    embeddings = all_embeddings[valid_indices]
    filtered_articles = [articles[i] for i in valid_indices]
    
    # Store embeddings in articles for later use
    for i, orig_idx in enumerate(valid_indices):
        articles[orig_idx]["embedding"] = all_embeddings[orig_idx].tolist()  # type: ignore
    
    logger.info("Processing %d unique articles after deduplication", len(filtered_articles))
    
    # Step 3: Cluster articles
    labels = cluster_articles(embeddings)
    
    # Step 4: Calculate weights
    weights = _calculate_weights(filtered_articles)
    now = datetime.utcnow()
    
    # Step 5: Build events
    events: list[dict] = []
    
    for label_id in sorted(set(labels)):
        # Find all indices for this cluster
        cluster_mask = np.array([l == label_id for l in labels])
        cluster_local_indices = np.where(cluster_mask)[0].tolist()
        
        if not cluster_local_indices:
            logger.debug("Skipping empty cluster with label %s", label_id)
            continue
        
        # Handle noise points (-1) as standalone events
        if label_id == -1:
            for local_idx in cluster_local_indices:
                events.append({
                    "event_id": f"standalone_{valid_indices[local_idx]}",
                    "label": filtered_articles[local_idx].get("title", "Standalone Article"),
                    "article_indices": [valid_indices[local_idx]],
                    "size": 1,
                    "weight_score": round(float(weights[local_idx]), 4),  # type: ignore
                    "representative_idx": valid_indices[local_idx],
                    "is_cluster": False,
                    "lifecycle": "emerging"
                })
            continue
        
        # Find representative article
        try:
            rep_local_idx = _find_representative(cluster_local_indices, embeddings)
            rep_article_idx = valid_indices[rep_local_idx]
        except ValueError as e:
            logger.error("Error finding representative for cluster %s: %s", label_id, e)
            continue
        except (IndexError, KeyError) as e:
            logger.error("Index error in representative selection: %s", e)
            continue
        
        # Get cluster label from representative
        rep_article = filtered_articles[rep_local_idx]
        cluster_label = rep_article.get("title", f"Event {label_id}")
        
        # Calculate cluster weight
        cluster_weight = float(np.sum(weights[cluster_local_indices]))  # type: ignore
        
        # Calculate average age
        ages_hours: list[float] = []
        for local_idx in cluster_local_indices:
            pub_str = str(filtered_articles[local_idx].get("published_at", ""))
            if pub_str:
                try:
                    pub = datetime.fromisoformat(pub_str.replace('Z', '+00:00'))
                    dt = (now - pub.replace(tzinfo=None)).total_seconds() / 3600
                    ages_hours.append(float(max(0.0, dt)))
                except Exception:
                    ages_hours.append(6.0)
            else:
                ages_hours.append(6.0)
        
        avg_age = sum(ages_hours) / len(ages_hours) if ages_hours else 6.0
        
        # Determine lifecycle
        lifecycle = _determine_lifecycle(len(cluster_local_indices), avg_age)
        
        # Build event
        events.append({
            "event_id": f"cluster_{label_id}",
            "label": cluster_label,
            "article_indices": [valid_indices[i] for i in cluster_local_indices],
            "size": len(cluster_local_indices),
            "weight_score": round(cluster_weight, 4),
            "representative_idx": rep_article_idx,
            "is_cluster": True,
            "lifecycle": lifecycle
        })
    
    # Sort by weight (descending) then by size (descending)
    events.sort(key=lambda e: (-e["weight_score"], -e["size"]))
    
    logger.info(
        "Detected %d events: %d clusters, %d standalone",
        len(events),
        sum(1 for e in events if e["is_cluster"]),
        sum(1 for e in events if not e["is_cluster"])
    )
    
    return events

"""
Semantic similarity and vector embedding module.
Uses SentenceTransformers (all-MiniLM-L6-v2) for deep contextual embeddings,
with an intelligent fallback to TF-IDF / Sublinear n-gram Cosine Vectorizer.
"""

import os
import logging
from typing import List, Tuple, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)

# Ensure Hugging Face operates offline from local cache without network retry delays
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

_MODEL_INSTANCE = None
_MODEL_NAME = "all-MiniLM-L6-v2"
_ENGINE_STATUS = "uninitialized"


def _load_sentence_transformer():
    """Attempt to load SentenceTransformer model with local cache preference."""
    global _MODEL_INSTANCE, _ENGINE_STATUS
    if _MODEL_INSTANCE is not None:
        return _MODEL_INSTANCE

    try:
        from sentence_transformers import SentenceTransformer
        _MODEL_INSTANCE = SentenceTransformer(_MODEL_NAME)
        _ENGINE_STATUS = f"SentenceTransformer ({_MODEL_NAME})"
        logger.info(f"Loaded SentenceTransformer: {_MODEL_NAME}")
        return _MODEL_INSTANCE
    except Exception as e:
        logger.warning(f"SentenceTransformer fallback: {e}")
        _ENGINE_STATUS = "TF-IDF N-Gram Vectorizer (Fallback)"
        return None


def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculate cosine similarity between two 1D or 2D vectors."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    sim = np.dot(vec_a, vec_b) / (norm_a * norm_b)
    # Clamp to [0.0, 1.0]
    return float(max(0.0, min(1.0, sim)))


def _tfidf_similarity(target_text: str, candidate_texts: List[str]) -> List[float]:
    """Fallback cosine similarity using scikit-learn TF-IDF with sublinear tf & 1-3 n-grams."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    corpus = [target_text] + candidate_texts
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        sublinear_tf=True,
        stop_words="english",
        max_features=5000
    )
    try:
        matrix = vectorizer.fit_transform(corpus)
        target_vec = matrix[0:1]
        cand_vecs = matrix[1:]
        sims = cosine_similarity(target_vec, cand_vecs)[0]
        return [float(max(0.0, min(1.0, s))) for s in sims]
    except Exception as e:
        logger.error(f"TF-IDF similarity failed: {e}")
        return [0.5 for _ in candidate_texts]


def compute_semantic_similarity(jd_text: str, resume_texts: List[str]) -> Tuple[List[float], Dict[str, str]]:
    """
    Computes semantic similarity scores (0.0 to 1.0) between a Job Description and a list of resumes.
    Returns (scores, engine_info).
    """
    if not resume_texts:
        return [], {"engine": "none", "model": "none"}

    model = _load_sentence_transformer()

    if model is not None:
        try:
            # Generate embeddings
            all_texts = [jd_text] + resume_texts
            embeddings = model.encode(all_texts, convert_to_numpy=True, normalize_embeddings=True)
            
            jd_emb = embeddings[0]
            scores = []
            for i in range(1, len(embeddings)):
                sim = _cosine_similarity(jd_emb, embeddings[i])
                scores.append(round(sim, 4))

            return scores, {"engine": "SentenceTransformers", "model": _MODEL_NAME}
        except Exception as e:
            logger.warning(f"Embedding computation error ({e}), falling back to TF-IDF.")

    # Fallback path
    scores = _tfidf_similarity(jd_text, resume_texts)
    return [round(s, 4) for s in scores], {"engine": "TF-IDF N-Gram Vectorizer", "model": "scikit-learn"}


def get_engine_status() -> str:
    """Returns current active embedding engine status."""
    global _ENGINE_STATUS
    if _ENGINE_STATUS == "uninitialized":
        _load_sentence_transformer()
    return _ENGINE_STATUS

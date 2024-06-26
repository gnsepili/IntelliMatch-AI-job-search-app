"""Module for matching jobs to resumes."""

import logging
from typing import List, Dict, Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class JobMatcher:
    """Class to match jobs to resumes based on embedding similarity."""

    @staticmethod
    def calculate_similarity(resume_embedding: np.ndarray, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate similarity between resume and job embeddings."""
        try:
            for job in jobs:
                similarity = cosine_similarity(
                    resume_embedding.reshape(1, -1),
                    job['embedding'].reshape(1, -1)
                )[0][0]
                job['similarity_score'] = float(similarity)
            return jobs
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            raise

    @staticmethod
    def rank_jobs(jobs: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """Rank jobs based on similarity score."""
        return sorted(jobs, key=lambda x: x['similarity_score'], reverse=True)[:top_n]
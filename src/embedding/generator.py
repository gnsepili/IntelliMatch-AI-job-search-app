"""Module for generating embeddings."""

import logging
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Class to generate embeddings for job descriptions."""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the EmbeddingGenerator with a specified model."""
        self.model = SentenceTransformer(model_name)

    def generate_job_embeddings(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for job descriptions."""
        try:
            for job in jobs:
                job['embedding'] = self.model.encode(job['description'])
            return jobs
        except Exception as e:
            logger.error(f"Error generating job embeddings: {e}")
            raise
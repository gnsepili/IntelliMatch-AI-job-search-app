"""Module for presenting job matches."""

from typing import List, Dict, Any

class JobPresenter:
    """Class to present matched jobs."""

    @staticmethod
    def present_jobs(ranked_jobs: List[Dict[str, Any]]) -> None:
        """Present ranked jobs."""
        for i, job in enumerate(ranked_jobs, 1):
            print(f"{i}. {job['title']}")
            print(f"   Similarity Score: {job['similarity_score']:.2f}")
            print(f"   Date Posted: {job['date_posted']}")
            print(f"   Description: {job['description'][:100]}...")
            print()
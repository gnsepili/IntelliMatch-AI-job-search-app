"""Main module for AI Job Matcher application."""

import logging
from typing import Dict, Any

from resume_processing.processor import ResumeProcessor
from job_scraping.scraper import LinkedInJobScraper
from embedding.generator import EmbeddingGenerator
from matching.matcher import JobMatcher
from presentation.presenter import JobPresenter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    """Main function to run the AI Job Matcher."""
    try:
        # Initialize components
        resume_processor = ResumeProcessor()
        job_scraper = LinkedInJobScraper()
        embedding_generator = EmbeddingGenerator()
        job_matcher = JobMatcher()
        job_presenter = JobPresenter()

        # Process resume
        resume_data = resume_processor.process_resume('Resume.pdf')
        
        # Scrape jobs
        job_title = input("Enter job title to search for: ")
        location = input("Enter location to search in: ")
        jobs = job_scraper.scrape_jobs(job_title, location)
        print(jobs)
        # Generate job embeddings
        jobs_with_embeddings = embedding_generator.generate_job_embeddings(jobs)
        
        # Calculate similarity and rank jobs
        matched_jobs = job_matcher.calculate_similarity(resume_data['embedding'], jobs_with_embeddings)
        top_jobs = job_matcher.rank_jobs(matched_jobs)
        
        # Present top jobs
        job_presenter.present_jobs(top_jobs)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
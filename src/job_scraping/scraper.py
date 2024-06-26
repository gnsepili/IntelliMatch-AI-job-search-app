"""Module for scraping job postings from LinkedIn."""

import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    """Class to scrape job postings from LinkedIn."""

    def __init__(self):
        """Initialize the LinkedInJobScraper with a Selenium WebDriver."""
        self.driver = self._setup_driver()

    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Selenium WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def scrape_jobs(self, job_title: str, location: str, days: int = 7) -> List[Dict[str, Any]]:
        """Scrape job postings for a given job title and location within the last n days."""
        url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
        self.driver.get(url)

        jobs = []
        page = 1
        while True:
            self._scroll_to_bottom()
            job_cards = self._get_job_cards()
            
            for card in job_cards:
                try:
                    job_data = self._extract_job_data(card)
                    if job_data and self._is_within_date_range(job_data['date_posted'], days):
                        jobs.append(job_data)
                except Exception as e:
                    logger.error(f"Error extracting job data: {e}")

            if not self._next_page(page):
                break
            page += 1

        self.driver.quit()
        return jobs

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the page to load all job listings."""
        SCROLL_PAUSE_TIME = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _get_job_cards(self) -> List:
        """Get all job cards from the current page."""
        return self.driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

    def _extract_job_data(self, card) -> Dict[str, Any]:
        """Extract relevant data from a job card."""
        try:
            title = card.find_element(By.CLASS_NAME, "base-search-card__title").text
            company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
            location = card.find_element(By.CLASS_NAME, "job-search-card__location").text
            date_posted = card.find_element(By.CLASS_NAME, "job-search-card__listdate").get_attribute("datetime")
            
            # Click on the card to load job details
            card.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
            )
            description = self.driver.find_element(By.CLASS_NAME, "show-more-less-html__markup").text

            return {
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted,
                "description": description
            }
        except Exception as e:
            logger.error(f"Error extracting data from job card: {e}")
            return None

    def _is_within_date_range(self, date_posted: str, days: int) -> bool:
        """Check if the job was posted within the specified number of days."""
        post_date = datetime.fromisoformat(date_posted)
        return datetime.now() - post_date <= timedelta(days=days)

    def _next_page(self, current_page: int) -> bool:
        """Navigate to the next page of job listings if available."""
        try:
            next_button = self.driver.find_element(By.XPATH, f"//button[@aria-label='Page {current_page + 1}']")
            next_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results__list-item"))
            )
            return True
        except:
            return False
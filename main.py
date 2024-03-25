from autoapply.autoapply import JobScraper
import os
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("API_KEY")
RESUME_PATH = os.getenv("RESUME_PATH")
profile_path = os.getenv("PROFILE_PATH")
job_scraper = JobScraper(api_key=API_KEY, 
                         profile_path=profile_path, 
                         resume_path=RESUME_PATH)
job_scraper.scrape_jobs()
job_scraper.run_gui()
job_scraper.process_links()

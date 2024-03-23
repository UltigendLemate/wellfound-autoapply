from autoapply.autoapply import JobScraper

job_scraper = JobScraper(api_key="AIzaSyD2R7Ao", 
                         profile_path=r"C:\Users\raman\AppData\Roaming\Mozilla\Firefox\Profiles\r2eazyi9.default-release", 
                         resume_path=r"C:\Users\raman\Downloads\RESUME.pdf")
job_scraper.scrape_jobs()
job_scraper.run_gui()
job_scraper.process_links()

from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from autoapply.helper.gui import GUI
from autoapply.helper.gotolink import Gotolink
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

class JobScraper:
    def __init__(self):
        self.options = FirefoxOptions()
        profile_path = os.getenv("PROFILE_PATH")

        self.options.profile = webdriver.FirefoxProfile(profile_path)
        self.driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=self.options)
        self.driver.get('https://wellfound.com/jobs')
        self.data = []

    def scrape_jobs(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True: 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        job_postings = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".styles_component__uTjje")
            )
        )

        for company in job_postings:
            try: 
                company_name = company.find_element(By.CSS_SELECTOR, ".styles_name__zvQcy").text
                roles = company.find_elements(By.CSS_SELECTOR, "a.styles_jobLink__US40J")
                for role in roles:
                    role_link = role.get_attribute("href")
                    role_title = role.find_element(By.CSS_SELECTOR, ".styles_title__xpQDw").text
                    role_stipend = role.find_element(By.CSS_SELECTOR, ".styles_compensation__3JnvU").text

                    role_locations = role.find_elements(By.CSS_SELECTOR, ".styles_location__O9Z62")
                    role_location = ""
                    for loc in role_locations:
                        role_location += loc.text + ","
                    self.data.append({"company": company_name, "role": role_title, "location": role_location, "stipend": role_stipend, "link": role_link})
            except Exception as e:
                print('Error:', e)
                continue

    def run_gui(self):
        gui = GUI(self.data)

    def process_links(self):
        gotolink = Gotolink()
        gotolink.process_links(d=self.data)

        time.sleep(50)


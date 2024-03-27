from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
from selenium.common.exceptions import InvalidSessionIdException
from autoapply.helper.genai import CoverLetterGenerator
import os
from dotenv import load_dotenv
from autoapply.helper.excel_handler import ExcelHandler

load_dotenv()  # Load variables from .env file

class Gotolink:
    def __init__(self):
        self.options = FirefoxOptions()
        profile_path = os.getenv("PROFILE_PATH")
        self.options.profile = webdriver.FirefoxProfile(profile_path)
        self.driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=self.options)
        self.data = []
        self.excel_handler = ExcelHandler()

    def process_link(self, link, d,k, lock):
        with lock:  # Ensure exclusive tab access
            try:
                self.driver.execute_script("window.open('');")  # Open a new tab
                self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the new tab
                self.driver.get(link)
                jobDesc = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "styles_description__uLHQ_"))
                )
                text = jobDesc.text
                coverletter = CoverLetterGenerator()
                cover_letter = coverletter.generate_cover_letter(job_description=text)
                applyButton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "styles_applyButton__k2sNa"))
                )
                applyButton.click()
                textArea = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "styles_component__kpbt6"))
                )
                textArea.send_keys(cover_letter)
                send_application_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='JobApplicationModal--SubmitButton']"))
                )
                print("application status sent for", link)
                print(cover_letter,"\n\n")
                # comment if testing
                send_application_button.click()
                self.excel_handler.add_application(link, text, cover_letter)
                self.excel_handler.save_excel()
                time.sleep(5)
            except Exception as e:
                print("Error:", e)
            finally:
                try:
                    self.driver.close()  # Close the current tab
                    self.driver.switch_to.window(self.driver.window_handles[0])  # Switch back to the main tab
                except InvalidSessionIdException:
                    print("Session lost, restarting driver...")
                    self.restart_driver()

    def process_links(self, d):
        self.driver.get('https://wellfound.com/jobs')
        lock = threading.Lock()
        threads = []
        i =0;
        print(d)
        for link in d:
            i+=1
            if link["checked"] == '0':
                continue
            print(link["company"], "\n\n\n\n")
            thread = threading.Thread(target=self.process_link, args=(link["link"], d,i, lock,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        print("loop ended")
        self.driver.quit()
    def processTeamLinks(self, teamMemberLinks,d, k):
        self.driver.execute_script("window.open('');")  # Open a new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the new tab
        for i in teamMemberLinks:
            self.driver.get(i)
            try:
                socials = WebDriverWait(self.driver,5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"..darkest.dir--profiles__show.profiles-show.file--links.links._a._jm a"))
                        )
                socialLinks = []
                for social in socials:
                    socialLinks.append(social.get_attribute("href"))
                print(socials)
            except :
                print("no socials of",i)
            

        

    def restart_driver(self):
        options = FirefoxOptions()
        profile_path = os.getenv("PROFILE_PATH")
        options.profile = webdriver.FirefoxProfile(profile_path)
        self.driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

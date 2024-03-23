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
                # send_application_button.click()
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


# d= [
#     {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '1'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Zenskar', 'role': 'Frontend Engineer Intern', 'location': 'India,Remote only,', 'stipend': '₹4L – ₹6L • No equity', 'link': 'https://wellfound.com/jobs/2610609-frontend-engineer-intern', 'checked': '0'}, {'company': 'Zenskar', 'role': 'DevOps Intern', 'location': 'India,Remote only,', 'stipend': '₹25,000 – ₹40,000 • No equity', 'link': 'https://wellfound.com/jobs/2925498-devops-intern', 'checked': '0'}, {'company': 'Zenskar', 'role': 'Backend Engineer Intern', 'location': 'India,Remote only,', 'stipend': '₹4L – ₹6L • No equity', 'link': 'https://wellfound.com/jobs/2610612-backend-engineer-intern', 'checked': '0'}, {'company': 'eSamudaay', 'role': 'Backend Engineer -Intern', 'location': 'Mangaluru,Udupi,Manipal,Remote only,', 'stipend': '₹1.8L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2957970-backend-engineer-intern', 'checked': '0'}, {'company': 'AST Consulting', 'role': 'Cyber security - Intern', 'location': 'Noida,Remote only,', 'stipend': '₹1.8L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/2763909-cyber-security-intern', 'checked': '0'}, {'company': 'Brenin Technologies', 'role': 'Google dialogflow developer', 'location': 'Jaipur,Remote only,', 'stipend': '₹1L – ₹2L • No equity', 'link': 'https://wellfound.com/jobs/2841304-google-dialogflow-developer', 'checked': '0'}, {'company': 'Tutcart', 'role': 'Quality Assurance Intern', 'location': 'Delhi,Gurgaon,Faridabad,Noida,New Delhi,More,Onsite or remote,', 'stipend': '₹60,000 – ₹1.8L • No equity', 'link': 'https://wellfound.com/jobs/2960306-quality-assurance-intern', 'checked': '0'}, {'company': 'Tutcart', 'role': 'QA Analyst', 'location': 'Delhi,Gurgaon,Noida,New Delhi,Delhi,More,Onsite or remote,', 'stipend': '₹60,000 – ₹1.5L • No equity', 'link': 'https://wellfound.com/jobs/2947625-qa-analyst', 'checked': '0'}, {'company': 'Lincode Labs', 'role': 'Machine Learning Intern- 3D', 'location': 'Bengaluru,Onsite or remote,', 'stipend': '₹1.8L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2953154-machine-learning-intern-3d', 'checked': '1'}, {'company': 'Asynq', 'role': 'Machine Learning Engineer', 'location': 'India,Remote only,', 'stipend': '₹15,000 – ₹30,000', 'link': 'https://wellfound.com/jobs/2752707-machine-learning-engineer', 'checked': '1'}, {'company': 'Wysa', 'role': 'Full Stack Engineer Intern', 'location': 'India,Remote only,', 'stipend': '₹20,000 – ₹30,000 • No equity', 'link': 'https://wellfound.com/jobs/2898947-full-stack-engineer-intern', 'checked': '1'}, {'company': 'SaralTech', 'role': 'Unity Stripe Animation Developer', 'location': 'India,Remote only,', 'stipend': '₹20,000 – ₹25,000', 'link': 'https://wellfound.com/jobs/2884728-unity-stripe-animation-developer', 'checked': '0'}, {'company': 'SaralTech', 'role': 'Unity Asset Designer Internship', 'location': 'India,Remote only,', 'stipend': '₹20,000 – ₹30,000', 'link': 'https://wellfound.com/jobs/2889335-unity-asset-designer-internship', 'checked': '1'}, {'company': 'Crio.Do', 'role': 'Subject Matter Expert -Low Level Design (LLD)', 'location': 'Bangalore Urban,Remote only,', 'stipend': '₹3L – ₹5L • No equity', 'link': 'https://wellfound.com/jobs/2706611-subject-matter-expert-low-level-design-lld', 'checked': '0'}, {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '1'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Petmojo', 'role': 'Flutter Developer', 'location': 'New Delhi,Remote only,', 'stipend': '₹20,000 – ₹30,000 • No equity', 'link': 'https://wellfound.com/jobs/2396575-flutter-developer', 'checked': '0'}, {'company': 'interactly.video', 'role': 'NodeJs Backend Developer Intern', 'location': 'Hyderabad,Onsite or remote,', 'stipend': '₹1L – ₹1.5L • 0.0% – 5.0%', 'link': 'https://wellfound.com/jobs/2334204-nodejs-backend-developer-intern', 'checked': '0'}, {'company': 'Dyumnin Semiconductors', 'role': 'Intern ASIC/FPGA design and Verification.', 'location': 'Bengaluru,Onsite or remote,', 'stipend': '₹2L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/624286-intern-asic-fpga-design-and-verification', 'checked': '0'}, {'company': 'Engaj Media', 'role': 'Mobile App Development', 'location': 'India,Onsite or remote,', 'stipend': '₹15,000 – ₹25,000 • No equity', 'link': 'https://wellfound.com/jobs/2937255-mobile-app-development', 'checked': '0'}, {'company': 'Red panda games', 'role': 'software intern mobile games Unity developer', 'location': 'Bengaluru,Remote only,', 'stipend': '₹60,000 – ₹4L', 'link': 'https://wellfound.com/jobs/2669318-software-intern-mobile-games-unity-developer', 'checked': '0'}, {'company': 'Mahawanti Solutions', 'role': 'Android developer intern', 'location': 'India,Onsite or remote,', 'stipend': '₹10,000 – ₹30,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2924399-android-developer-intern', 'checked': '0'}, {'company': 'Mahawanti Solutions', 'role': 'Software Developer intern', 'location': 'India,Onsite or remote,', 'stipend': '₹10,000 – ₹30,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2916122-software-developer-intern', 'checked': '0'}, {'company': 'BigCircle', 'role': 'Software Engineering Intern (Web Dev)', 'location': 'India,Remote only,', 'stipend': '₹2.4L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/2866106-software-engineering-intern-web-dev', 'checked': '0'}, {'company': 'Listnr', 'role': 'ML Engineer Intern (Python)', 'location': 'India,Gurgaon,Remote only,', 'stipend': '₹4L – ₹5L • 0.1% – 0.2%', 'link': 'https://wellfound.com/jobs/948301-ml-engineer-intern-python', 'checked': '0'}, {'company': 'travokarma', 'role': 'React Native Web App Developer Intern', 'location': 'Bengaluru,Gurgaon,Hyderabad,Jaipur,Ahmedabad,More,Remote only,', 'stipend': '₹1.8L – ₹2.4L • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2886157-react-native-web-app-developer-intern', 'checked': '0'}, {'company': 'travokarma', 'role': 'App Development intern', 'location': 'Bengaluru,Delhi,Hyderabad,Jaipur,Mumbai,More,Remote only,', 'stipend': '₹1.65L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/1479779-app-development-intern', 'checked': '0'}, {'company': 'IELTS proficiency', 'role': 'iOS developer (Lidar scanning and AR tech)', 'location': 'Delhi,Remote only,', 'stipend': '₹72,000 – ₹1.5L • No equity', 'link': 'https://wellfound.com/jobs/2928368-ios-developer-lidar-scanning-and-ar-tech', 'checked': '0'}, {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '0'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '1'}, {'company': 'ScopeX Fintech', 'role': 'Mobile App Development Intern', 'location': 'Pune,Berlin,Remote only,', 'stipend': '₹1.2L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/2838602-mobile-app-development-intern', 'checked': '1'}]


# job = Gotolink()
# job.process_links(d)
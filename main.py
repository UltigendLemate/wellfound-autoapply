from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from gui import openGUI
from gotolink import process_links
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

options = FirefoxOptions()
profile_path = os.getenv("PROFILE_PATH")

options.profile = webdriver.FirefoxProfile(profile_path)

driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=options)
driver.get('https://wellfound.com/jobs')
data =[]
last_height = driver.execute_script("return document.body.scrollHeight")

while True: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



jobPostings =  WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".styles_component__uTjje")
            )
    )



for company in jobPostings:
    try : 
        companyName =  company.find_element(By.CSS_SELECTOR,".styles_name__zvQcy").text
        roles = company.find_elements(By.CSS_SELECTOR,"a.styles_jobLink__US40J")
        for role in roles:
            roleLink = role.get_attribute("href")
            roleTitle = role.find_element(By.CSS_SELECTOR,".styles_title__xpQDw").text
            roleStipend = role.find_element(By.CSS_SELECTOR,".styles_compensation__3JnvU").text

            roleLocations = role.find_elements(By.CSS_SELECTOR,".styles_location__O9Z62")
            roleLocation = ""
            for loc in roleLocations:
                roleLocation += loc.text +","
            data.append({"company":companyName,"role":roleTitle,"location":roleLocation,"stipend":roleStipend,"link":roleLink})
    except:
        print('error')
        continue


openGUI(data)
print(data)

process_links(data)

time.sleep(50)

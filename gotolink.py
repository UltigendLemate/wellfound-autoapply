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
from genai import generate_cover_letter
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file



def process_link(driver: webdriver, lock, link, link_dict):
    """Processes a single link, retrieving and printing the title."""
    with lock:  # Ensure exclusive tab access
        try:
            driver.execute_script("window.open('');")  # Open a new tab
            driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

            driver.get(link)

            jobDesc = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styles_description__uLHQ_"))
            )

            text = jobDesc.text
            cover_letter = generate_cover_letter(text)
            # print(text)
            applyButton = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "styles_applyButton__k2sNa"))
            )
            applyButton.click()
            textArea = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styles_component__kpbt6"))
            )
            textArea.send_keys(cover_letter)
            send_application_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='JobApplicationModal--SubmitButton']"))
            )
            # COMMENT IF TESTING
            # send_application_button.click()
            time.sleep(5);



            

        except Exception as e:
            print("p")  # Print informative error message
        finally:
            try:
                driver.close()  # Close the current tab
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab
            except InvalidSessionIdException:
                print("Session lost, restarting driver...")
                options = FirefoxOptions()
                profile_path = os.getenv("PROFILE_PATH")

                options.profile = webdriver.FirefoxProfile(profile_path)

                driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=options) # Recreate driver if session is lost




def process_links(d):
    options = FirefoxOptions()

    profile_path = os.getenv("PROFILE_PATH")

    options.profile = webdriver.FirefoxProfile(profile_path)

    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=options)
    driver.get('https://wellfound.com/jobs')

    lock = threading.Lock()
    threads = []
    link_dict={}
    for link in d:  
        if (link["checked"]=='0'):
            continue
        print(link["company"],"\n\n\n\n")
        thread = threading.Thread(target=process_link, args=(driver,lock,link["link"],link_dict,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  

    print("loop ended")
    driver.quit()



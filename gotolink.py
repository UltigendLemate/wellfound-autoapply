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
            send_application_button.click()
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

    
# d = [

#     {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '0'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Medblocks', 'role': 'Software Engineer', 'location': 'Delhi,Bangalore Urban,Onsite or remote,', 'stipend': '₹60,000 – ₹1.2L • No equity', 'link': 'https://wellfound.com/jobs/2945262-software-engineer', 'checked': '0'}, {'company': 'The Small Data Store', 'role': 'Software Engineer/ Full-stack developer', 'location': 'Pune,Remote only,', 'stipend': '₹60,000 – ₹1.2L • 0.5% – 1.0%', 'link': 'https://wellfound.com/jobs/2298873-software-engineer-full-stack-developer', 'checked': '1'}, {'company': 'SaralTech', 'role': 'Unity Stripe Animation Developer', 'location': 'India,Remote only,', 'stipend': '₹20,000 – ₹25,000', 'link': 'https://wellfound.com/jobs/2884728-unity-stripe-animation-developer', 'checked': '0'}, {'company': 'SaralTech', 'role': 'Unity Asset Designer Internship', 'location': 'India,Remote only,', 'stipend': '₹20,000 – ₹30,000', 'link': 'https://wellfound.com/jobs/2889335-unity-asset-designer-internship', 'checked': '0'}, {'company': 'Kraftbase', 'role': 'Frontend Developer intern', 'location': 'India,Remote only,', 'stipend': '₹1.8L – ₹1.8L • No equity', 'link': 'https://wellfound.com/jobs/2745907-frontend-developer-intern', 'checked': '1'}, {'company': 'Kraftbase', 'role': 'Backend engineer intern', 'location': 'India,Remote only,', 'stipend': '₹1.8L – ₹1.8L • No equity', 'link': 'https://wellfound.com/jobs/2849361-backend-engineer-intern', 'checked': '1'}, {'company': 'Kraftbase', 'role': 'Flutter Developer Intern', 'location': 'Dubai,India,Bangladesh,Sri Lanka,Remote only,', 'stipend': '₹1.8L – ₹1.8L • No equity', 'link': 'https://wellfound.com/jobs/2811955-flutter-developer-intern', 'checked': '0'}, {'company': 'Leap Wallet', 'role': 'Software Development Engineer Intern - Frontend', 'location': 'India,Remote only,', 'stipend': '₹4L – ₹8L • No equity', 'link': 'https://wellfound.com/jobs/2946147-software-development-engineer-intern-frontend', 'checked': '1'}, {'company': 'Laxaar', 'role': 'ReactJS Developer-Remote', 'location': 'India,Chandigarh,Ahmedabad,Gujarat,Mohali,Remote only,', 'stipend': '₹1.1L – ₹1.2L • No equity', 'link': 'https://wellfound.com/jobs/2947967-reactjs-developer-remote', 'checked': '1'}, {'company': 'interactly.video', 'role': 'NodeJs Backend Developer Intern', 'location': 'Hyderabad,Onsite or remote,', 'stipend': '₹1L – ₹1.5L • 0.0% – 5.0%', 'link': 'https://wellfound.com/jobs/2334204-nodejs-backend-developer-intern', 'checked': '0'}, {'company': 'Tutcart', 'role': 'QA Analyst - Manual Testing', 'location': 'Delhi,New Delhi,Delhi,New Delhi,New Delhi,More,Remote only,', 'stipend': '₹60,000 – ₹1.2L • No equity', 'link': 'https://wellfound.com/jobs/2947625-qa-analyst-manual-testing', 'checked': '0'}, {'company': 'Petmojo', 'role': 'Flutter Developer', 'location': 'New Delhi,Remote only,', 'stipend': '₹20,000 – ₹30,000 • No equity', 'link': 'https://wellfound.com/jobs/2396575-flutter-developer', 'checked': '0'}, {'company': 'Dyumnin Semiconductors', 'role': 'Intern ASIC/FPGA design and Verification.', 'location': 'Bengaluru,Onsite or remote,', 'stipend': '₹2L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/624286-intern-asic-fpga-design-and-verification', 'checked': '0'}, {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '0'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Engaj Media', 'role': 'Mobile App Development', 'location': 'India,Onsite or remote,', 'stipend': '₹15,000 – ₹25,000 • No equity', 'link': 'https://wellfound.com/jobs/2937255-mobile-app-development', 'checked': '0'}, {'company': 'Briashta Games', 'role': 'Android developer intern at Briashta Games', 'location': 'Noida,New Delhi,Gurugram,Onsite or remote,', 'stipend': '₹1.2L – ₹1.8L • No equity', 'link': 'https://wellfound.com/jobs/2491169-android-developer-intern-at-briashta-games', 'checked': '0'}, {'company': 'Spenza', 'role': 'Frontend Engineer Intern – ReactJS', 'location': 'Bengaluru,Remote only,', 'stipend': '₹1L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/978721-frontend-engineer-intern-reactjs', 'checked': '1'}, {'company': 'Cypherock Wallet', 'role': 'C/C++ Programmer Intern', 'location': 'Delhi,New Delhi,Gurugram,Gurugram,Onsite or remote,', 'stipend': '₹1L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/474650-c-c-programmer-intern', 'checked': '0'}, {'company': 'Cypherock Wallet', 'role': 'Wordpress Developer (Intern)', 'location': 'Gurgaon,Onsite or remote,', 'stipend': '₹1.8L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/2779347-wordpress-developer-intern', 'checked': '1'}, {'company': 'Cypherock Wallet', 'role': 'Full Stack Developer Intern', 'location': 'Gurgaon,New Delhi,Gurugram,Onsite or remote,', 'stipend': '₹1.2L – ₹4L • No equity', 'link': 'https://wellfound.com/jobs/644670-full-stack-developer-intern', 'checked': '1'}, {'company': 'Zenskar', 'role': 'DevOps Intern', 'location': 'India,Remote only,', 'stipend': '₹25,000 – ₹40,000 • No equity', 'link': 'https://wellfound.com/jobs/2925498-devops-intern', 'checked': '0'}, {'company': 'Zenskar', 'role': 'Backend Engineer Intern', 'location': 'India,Remote only,', 'stipend': '₹4L – ₹6L • No equity', 'link': 'https://wellfound.com/jobs/2610612-backend-engineer-intern', 'checked': '0'}, {'company': 'Eatoes', 'role': 'Full Stack developer Intern', 'location': 'India,Remote only,', 'stipend': '₹30,000 – ₹60,000', 'link': 'https://wellfound.com/jobs/2924532-full-stack-developer-intern', 'checked': '1'}, {'company': 'Mahawanti Solutions', 'role': 'Android developer intern', 'location': 'India,Onsite or remote,', 'stipend': '₹10,000 – ₹30,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2924399-android-developer-intern', 'checked': '0'}, {'company': 'Mahawanti Solutions', 'role': 'AI/Machine learning intern', 'location': 'India,Onsite or remote,', 'stipend': '₹15,000 – ₹35,000', 'link': 'https://wellfound.com/jobs/2916123-ai-machine-learning-intern', 'checked': '0'}, {'company': 'Mahawanti Solutions', 'role': 'Software Developer intern', 'location': 'India,Onsite or remote,', 'stipend': '₹10,000 – ₹30,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2916122-software-developer-intern', 'checked': '0'}, {'company': 'Loop', 'role': 'Backend engineering Intern', 'location': 'Bengaluru,Remote,Onsite or remote,', 'stipend': '₹3.6L – ₹6L • No equity', 'link': 'https://wellfound.com/jobs/2618390-backend-engineering-intern', 'checked': '0'}, {'company': 'Crio.Do', 'role': 'Subject Matter Expert -Low Level Design (LLD)', 'location': 'Bangalore Urban,Remote only,', 'stipend': '₹3L – ₹5L • No equity', 'link': 'https://wellfound.com/jobs/2706611-subject-matter-expert-low-level-design-lld', 'checked': '0'}, {'company': 'RD&X Network', 'role': 'Frontend Developer Intern (React Js)', 'location': 'Bangalore Urban,Onsite or remote,', 'stipend': '₹1.2L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2241204-frontend-developer-intern-react-js', 'checked': '1'}, {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '0'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Red panda games', 'role': 'software intern mobile games Unity developer', 'location': 'Bengaluru,Remote only,', 'stipend': '₹60,000 – ₹4L', 'link': 'https://wellfound.com/jobs/2669318-software-intern-mobile-games-unity-developer', 'checked': '0'}, {'company': 'Listnr', 'role': 'ML Engineer Intern (Python)', 'location': 'India,Gurgaon,Remote only,', 'stipend': '₹4L – ₹5L • 0.1% – 0.2%', 'link': 'https://wellfound.com/jobs/948301-ml-engineer-intern-python', 'checked': '0'}, {'company': 'IELTS proficiency', 'role': 'iOS developer (Lidar scanning and AR tech)', 'location': 'Delhi,Remote only,', 'stipend': '₹72,000 – ₹1.5L • No equity', 'link': 'https://wellfound.com/jobs/2928368-ios-developer-lidar-scanning-and-ar-tech', 'checked': '0'}, {'company': 'ScopeX Fintech', 'role': 'Mobile App Development Intern', 'location': 'Pune,Berlin,Remote only,', 'stipend': '₹1.2L – ₹3L • No equity', 'link': 'https://wellfound.com/jobs/2838602-mobile-app-development-intern', 'checked': '0'}, {'company': 'StackPro', 'role': 'Software Developer Intern', 'location': 'Bengaluru,Onsite or remote,', 'stipend': '₹1.5L – ₹2.5L • No equity', 'link': 'https://wellfound.com/jobs/979839-software-developer-intern', 'checked': '1'}, {'company': 'CRUV', 'role': 'Flutter Developer', 'location': 'India,Remote only,', 'stipend': '₹1.2L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2506429-flutter-developer', 'checked': '0'}, {'company': 'CRUV', 'role': 'Python Developer in Product based company.', 'location': 'India,Remote only,', 'stipend': '₹1.2L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2534476-python-developer-in-product-based-company', 'checked': '0'}, {'company': 'CRUV', 'role': 'Data Scientist in Product based company.', 'location': 'India,Remote only,', 'stipend': '₹1.2L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/2749858-data-scientist-in-product-based-company', 'checked': '0'}, {'company': 'travokarma', 'role': 'React Native Web App Developer Intern', 'location': 'Bengaluru,Gurgaon,Hyderabad,Jaipur,Ahmedabad,More,Remote only,', 'stipend': '₹1.8L – ₹2.4L • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2886157-react-native-web-app-developer-intern', 'checked': '0'}, {'company': 'travokarma', 'role': 'App Development intern', 'location': 'Bengaluru,Delhi,Hyderabad,Jaipur,Mumbai,More,Remote only,', 'stipend': '₹1.65L – ₹2.4L • No equity', 'link': 'https://wellfound.com/jobs/1479779-app-development-intern', 'checked': '0'}, {'company': 'Edzeup', 'role': 'Backend Intern', 'location': 'India,Bangalore Urban,Remote only,', 'stipend': '₹1L – ₹2L • No equity', 'link': 'https://wellfound.com/jobs/2878516-backend-intern', 'checked': '1'}, {'company': 'VCBay', 'role': 'Flutter App Developer', 'location': 'India,Remote only,', 'stipend': '₹84,000 – ₹1.2L • No equity', 'link': 'https://wellfound.com/jobs/2488521-flutter-app-developer', 'checked': '0'}, {'company': 'stealth startup', 'role': 'Internship : Android developer/Full Stack Developer', 'location': 'Bangalore Urban,Remote only,', 'stipend': '₹10,000 – ₹25,000 • No equity', 'link': 'https://wellfound.com/jobs/2871260-internship-android-developer-full-stack-developer', 'checked': '0'}, {'company': 'Tara Capital Partners India', 'role': 'Quant Trader/Researcher', 'location': 'In office,', 'stipend': '₹10L – ₹40L • No equity', 'link': 'https://wellfound.com/jobs/2268796-quant-trader-researcher', 'checked': '0'}, {'company': 'Mutant (X)', 'role': 'Webflow Developer', 'location': 'Onsite or remote,', 'stipend': '₹45,000 – ₹80,000 • 0.0% – 1.0%', 'link': 'https://wellfound.com/jobs/2925834-webflow-developer', 'checked': '0'}, {'company': 'Lamatic', 'role': 'Founding Engineering - LLM (Internship)', 'location': 'Europe,India,United States,Remote only,', 'stipend': '₹3L – ₹6L • No equity', 'link': 'https://wellfound.com/jobs/2885703-founding-engineering-llm-internship', 'checked': '0'}]



# process_links(d)

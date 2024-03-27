import google.generativeai as genai
import os
from dotenv import load_dotenv
from autoapply.helper.pdfhandler import PDFHandler

load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("API_KEY")
RESUME_PATH = os.getenv("RESUME_PATH")
genai.configure(api_key=API_KEY)

class CoverLetterGenerator:
    def __init__(self, model_name="gemini-1.0-pro-001"):
        self.model_name = model_name
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

        self.pdflinks = PDFHandler(RESUME_PATH)

    def generate_cover_letter(self, job_description: str) -> str:
        try:
            project_links = self.pdflinks.extract_links()
            resume_text = self.pdflinks.extract_text()
        except FileNotFoundError:
            print(f"Error: File '{RESUME_PATH}' not found.")
        except UnicodeDecodeError:
            print("Error: Unable to decode the file using UTF-8 encoding.")

        prompt = f"""
        My Resume : 
        "{resume_text}"

        Create a custom brief cover letter (to enter on a job portal) for the following job description :

        "{job_description}"
        Here is links of my all projects and userhandles for mail and various other profiles use these links where there are relevant. Here the list of all links "{project_links} use actual links dont just use link keyword give actual projects links in cover letter"

        Ensure the cover letter is brief (not more than 5-6 lines). Make the cover letter stand out. try some quirky statements. but ensure to keep it professional. Tone down the vocabulary to sound like a college student. Do not use heavy words. Do not be informal. Be polite. If you mention any projects (encouraged to do), then include their link as well from resume.  
        Strictly Do not include any variable, or greetings or footer (signing off) in the response. dont include any variables. recheck twice. include links."""
        
        response = self.model.generate_content(prompt)
        return response.text

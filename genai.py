import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

genai.configure(api_key=os.getenv("API_KEY"))

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def generate_cover_letter(job_description: str) -> str:
    prompt = f"""
    My Resume : 
    "CHAITANYA ANAND

    +91 9711091823 Github Profile Linkedin Profile chaitanya.anand@gmail.com
    EXPERIENCE
    Founder, Fresources December 2021 - Present
    ● Spearheaded the development of the frontend of the Fresources platform, leveraging cutting-edge technologies
    and industry best practices.
    ● The platform has earned the trust of over 20,000 students in Delhi and 4 Million page views till now.
    ● Led and managed a team of 150+ contributors. Provided technical guidance and mentorship.
    ● Implemented multiple iterations of the Fresources website, culminating in the release of v3, which includes
    innovative features such as an events page, like/favorite resources, resulting in a 30% increase in user
    engagement and a 15% decrease in bounce rate.
    Website Developer, Carboledger June 2023 - July 2023
    ● Successfully transferred website blogs to WordPress while preserving the original Next.js design, ensuring a
    smooth transition and improved content management efficiency.
    ● Enhanced website performance and user engagement by integrating HubSpot.
    ● Implemented SEO best practices, and configured precise meta descriptions, and optimized search visibility with
    Google Analytics and Search Console.
    Freelancer | View All Projects December 2021 - May 2023
    ● Built numerous landing pages and frontend websites. Some of them are listed below:
    ● Hammer - Built on wordpress from scratch. Includes payment integration for subscription (avg 20 users
    pm). Regular magazine uploads and push notifications to users. Magazines can be viewed in 3d.
    ● Growth Rocket - Contributed to a visually stunning Next.js portfolio website, incorporating smooth
    animations and transitions that led to a remarkable 200% surge in sales.

    PROJECTS
    Synapse — Github | Demo | Nextjs 13, Tailwind, Supabase, Drizzle, Sockets, Quill (https://www.linkedin.com/posts/chaitanyanand_level-up-your-workflow-my-journey-of-building-activity-7148726982850019328-QuJj/)
    ● Developed a collaborative web application with real-time features for enhanced productivity.
    ● Designed a responsive UI that adapts flawlessly to various devices, ensuring accessibility across platforms. It
    includes the option to change theme (light or dark) as well.
    ● Engineered real-time cursor and selection tracking for seamless multi-user collaboration, fostering teamwork and
    efficiency.
    ● Integrated a payment gateway (Stripe) to unlock premium features.
    Cryptic Hunt— Link | Github | Bcrypt, Express, JWT, MongoDB, Pug, Material CSS
    ● Created a full stack application using JWT for secure user authentication, enabling an event for 400+ participants.
    ● Implemented a real-time leaderboard and level progression system based on correct answers.
    ● Deployed the application on Vercel, secured with Cloudflare, ensuring a reliable and fortified platform.
    ● Addressed vulnerabilities, ensured a secure environment for participants, and safeguarded user data. Achieved an
    exceptional track record of 100% uptime and 0 security breaches.
    Quik Planr— Github | Next Js, React Js, Tailwind, Swiper (https://devfolio.co/projects/quikplanr-5f4f)
    ● Developed Quik Planr, a Next.js application that leverages generative AI and prompt engineering to transform
    two-line ideas into comprehensive market research plans.
    ● Crafted a sleek, intuitive interface that even first-time entrepreneurs could navigate with ease. Reduced loading
    time by 60% (from 10s to 4s) through optimized techniques.

    ● Languages: Python, Javascript, C++, SQL
    ● Frameworks: React, Next, Vue, Tailwind, Pug, Express, Bootstrap
    ● Tools: Git, MongoDB, Numpy, GPT Prompt, AWS, VSCode, Vercel, Burpsuite, Nmap, Wireshark,Notion, Cypress
    ACHIEVEMENTS
    ● 3rd Prize at Scythe CTF (Capture The Flag) organized by Cognizance IIT Roorkee.
    ● 1st Rank at MSIT Google Developer Student Club’s Hack-A-Miner Hackathon
    ● 1st Rank at Delhi Technological University’s IT Department Hackathon
    ● 1st Rank at Chitkara University’s All India Tech Hack 3.0
    ● Finalist at Sparkathon conducted by Walmart Technologies 2023
    ● 2nd Prize at Code Kshetra - JIMS
    ● Solved 400+ Data Structures and Algorithms Questions collectively on all platforms


    "

    My best projects are synapse and quikplanr. Their links are https://shortenn.me/chaitanya-synapse and https://shortenn.me/chaitanya-quikplanr respectively. Use only these links wherever necessary
    Create a custom brief cover letter (to enter on a job portal) for the following job description :

    "{job_description}"

    Ensure the cover letter is brief (not more than 5-6 lines). Make the cover letter stand out. try some quirky statements. but ensure to keep it professional. Tone down the vocabulary to sound like a college student. Do not use heavy words. Do not be informal. Be polite. If you mention any projects, then include their link as well from resume. Do not include any variable, or greetings or footer (signing off) in the cover letter."""
    response  = model.generate_content(prompt)
    print(response.text)
    return response.text


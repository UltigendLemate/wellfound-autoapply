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

prompt_parts = [
  "My Resume : \n\"CHAITANYA ANAND\n\n+91 9711091823 Github Profile Linkedin Profile chaitanya.anand@gmail.com\nEXPERIENCE\nFounder, Fresources December 2021 - Present\n● Spearheaded the development of the frontend of the Fresources platform, leveraging cutting-edge technologies\nand industry best practices.\n● The platform has earned the trust of over 20,000 students in Delhi and 4 Million page views till now.\n● Led and managed a team of 150+ contributors. Provided technical guidance and mentorship.\n● Implemented multiple iterations of the Fresources website, culminating in the release of v3, which includes\ninnovative features such as an events page, like/favorite resources, resulting in a 30% increase in user\nengagement and a 15% decrease in bounce rate.\nWebsite Developer, Carboledger June 2023 - July 2023\n● Successfully transferred website blogs to WordPress while preserving the original Next.js design, ensuring a\nsmooth transition and improved content management efficiency.\n● Enhanced website performance and user engagement by integrating HubSpot.\n● Implemented SEO best practices, and configured precise meta descriptions, and optimized search visibility with\nGoogle Analytics and Search Console.\nFreelancer | View All Projects December 2021 - May 2023\n● Built numerous landing pages and frontend websites. Some of them are listed below:\n● Hammer - Built on wordpress from scratch. Includes payment integration for subscription (avg 20 users\npm). Regular magazine uploads and push notifications to users. Magazines can be viewed in 3d.\n● Growth Rocket - Contributed to a visually stunning Next.js portfolio website, incorporating smooth\nanimations and transitions that led to a remarkable 200% surge in sales.\n\nPROJECTS\nSynapse — Github | Demo | Nextjs 13, Tailwind, Supabase, Drizzle, Sockets, Quill (https://www.linkedin.com/posts/chaitanyanand_level-up-your-workflow-my-journey-of-building-activity-7148726982850019328-QuJj/)\n● Developed a collaborative web application with real-time features for enhanced productivity.\n● Designed a responsive UI that adapts flawlessly to various devices, ensuring accessibility across platforms. It\nincludes the option to change theme (light or dark) as well.\n● Engineered real-time cursor and selection tracking for seamless multi-user collaboration, fostering teamwork and\nefficiency.\n● Integrated a payment gateway (Stripe) to unlock premium features.\nCryptic Hunt— Link | Github | Bcrypt, Express, JWT, MongoDB, Pug, Material CSS\n● Created a full stack application using JWT for secure user authentication, enabling an event for 400+ participants.\n● Implemented a real-time leaderboard and level progression system based on correct answers.\n● Deployed the application on Vercel, secured with Cloudflare, ensuring a reliable and fortified platform.\n● Addressed vulnerabilities, ensured a secure environment for participants, and safeguarded user data. Achieved an\nexceptional track record of 100% uptime and 0 security breaches.\nQuik Planr— Github | Next Js, React Js, Tailwind, Swiper (https://devfolio.co/projects/quikplanr-5f4f)\n● Developed Quik Planr, a Next.js application that leverages generative AI and prompt engineering to transform\ntwo-line ideas into comprehensive market research plans.\n● Crafted a sleek, intuitive interface that even first-time entrepreneurs could navigate with ease. Reduced loading\ntime by 60% (from 10s to 4s) through optimized techniques.\n\n● Languages: Python, Javascript, C++, SQL\n● Frameworks: React, Next, Vue, Tailwind, Pug, Express, Bootstrap\n● Tools: Git, MongoDB, Numpy, GPT Prompt, AWS, VSCode, Vercel, Burpsuite, Nmap, Wireshark,Notion, Cypress\nACHIEVEMENTS\n● 3rd Prize at Scythe CTF (Capture The Flag) organized by Cognizance IIT Roorkee.\n● 1st Rank at MSIT Google Developer Student Club’s Hack-A-Miner Hackathon\n● 1st Rank at Delhi Technological University’s IT Department Hackathon\n● 1st Rank at Chitkara University’s All India Tech Hack 3.0\n● Finalist at Sparkathon conducted by Walmart Technologies 2023\n● 2nd Prize at Code Kshetra - JIMS\n● Solved 400+ Data Structures and Algorithms Questions collectively on all platforms\n\nMy best projects are synapse and quikplanr.\n\"\n\n\nCreate a custom brief cover letter (to enter on a job portal) for the following job description :\n\n\"We are looking for a Node.js Developer responsible for managing the interchange of data between the server and the users. Your primary focus will be the development of all server-side logic, definition and maintenance of the central database, and ensuring high performance and responsiveness to requests from the front-end. You will also be responsible for integrating the front-end elements built by your co-workers into the application. Therefore, a basic understanding of front-end technologies is necessary as well.\n\nResponsibilities\n\nIntegration of user-facing elements developed by front-end developers with server side logic.\nWriting reusable, testable, and efficient code.\nDesign and implementation of low-latency, high-availability, and performant applications.\nImplementation of security and data protection.\nWriting SQL queries and working with MySQL database.\nSkills And Qualifications\n\nGood knowledge with JavaScript.\nKnowledge of Node.js.\nUnderstanding the nature of asynchronous programming and its quirks and workarounds.\nUser authentication and authorization between multiple systems, servers, and environments.\nCreating database schemas that represent and support business processes.\nProficient understanding of code versioning tools, such as Git\"\n\nEnsure the cover letter is brief (not more than 5-6 lines). Ignore the greetings and footer (signing off). Makey the cover letter stand out. try some quirky statements. but ensure to keep it professional. also tone down the vocabulary to sound like a college student. Do not be informal. If you mention any projects, then include their link as well from resume.\n\n\n\n",
]


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


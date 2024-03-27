## What does it do?
This is a simple script that will automate the process of you applying to jobs on Wellfound. 
Demo Link : https://drive.google.com/file/d/13gwr3La3zDbLmOl15ouePoD5a4n-iznQ/view?usp=sharing

**Don't forget to change the basic prompt at genai.py file.**

Steps to make it work : 
 - [Install Firefox](#install-firefox)
 - [Install Geckodriver](#install-geckodriver)
 - [Set wellfound](#set-wellfound)
 - [Clone Repo](#clone-repo)
 - [Populate Env](#populate-env)

#### Install Firefox
Download Mozilla Firefox from [here](https://www.mozilla.org/en-US/firefox/new/). Currently the script runs only on your Firefox Browser


#### Install Geckodriver
Geckodriver is required by selenium to interact with firefox browser.
Install the driver supported by your os from assets from [here](https://github.com/mozilla/geckodriver/releases).


#### Set Wellfound
Open [wellfound.com](https://wellfound.com), set up your profile and set your desired filters at [wellfound.com/jobs](https://wellfound.com/jobs).


#### Clone repo
clone this repo. install dependencies using : 
```
pip install -r ./requirements.txt
```


#### Populate env
check the format of env variables in env.example file.

Run Main.py after doing all the above steps. Reach out to me incase of any issue.

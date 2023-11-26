r"""
    __  ___                  __               ____                  __                       ___         __                        __  _           
   /  |/  /___ _____ _____  / /____  _____   / __ \__  ____________/ /_  ____ _________     /   | __  __/ /_____  ____ ___  ____ _/ /_(_)___  ____ 
  / /|_/ / __ `/ __ `/_  / / __/ _ \/ ___/  / /_/ / / / / ___/ ___/ __ \/ __ `/ ___/ _ \   / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ / __ \/ __ \
 / /  / / /_/ / /_/ / / /_/ /_/  __/ /     / ____/ /_/ / /  / /__/ / / / /_/ (__  )  __/  / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/ / /_/ / / / /
/_/  /_/\__,_/\__, / /___/\__/\___/_/     /_/    \__,_/_/   \___/_/ /_/\__,_/____/\___/  /_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/ 
             /____/                                                                                                                                   
    @file: app.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 27th Nov 2023
    @error-series: 1100
    @description:
        - Main module of the application (Driver module).
        - Python Version: 3.10.5
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "0.0.0"

from time import sleep
from sys import exit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from components import ip, google_sheets, microsoft, magzter
from utilities import tools, scrap_tools

# Loading application settings
settings: dict = tools.loadAppSettings()
if not settings:
    # No settings found. Empty dictionary ({})
    print("No settings found. Error Code: 1101")
    exit(-1)


# Adding chrome options based on user settings
chromeOptions: Options = Options()
if not settings["chrome"]["display_images"]:
    chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
if settings["chrome"]["headless"]:
    chromeOptions.add_argument("--headless")

# Services
service = Service(
    executable_path=settings["chromedriver"]["executable_path"],
    port=settings["chromedriver"]["port"],
)

# Initializing the chrome webdriver
chrome: webdriver.Chrome = webdriver.Chrome(options=chromeOptions, service=service)

# Fetching URLs from settings
microsoftUrl: str = settings["url"]["microsoft"]
outlookUrl: str = settings["url"]["outlook"]
magzterUrl: str = settings["url"]["magzter"]


# Tab class to handling multiple tabs. It makes easy to switch between different tabs.
class Tab:
    Microsoft = 0
    Magzter = 1

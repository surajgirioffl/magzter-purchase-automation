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
from components import ip, google_sheets, microsoft, magzter
from utilities import tools, scrap_tools

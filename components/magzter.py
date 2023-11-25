"""
    @file: components/magzter.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 26th Nov 2023
    @error-series: 2400
    @description:
        * Module to perform any operations related to magzter for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utilities import scrap_tools


class Magzter:
    """
    Description:
        - Class to perform operations related to Magzter for the project.
    """

    def __init__(self, chromeInstance: Chrome) -> None:
        """
        Description:
            - Initializes a new instance of the class.

        Args:
            * chromeInstance (Chrome):
                - An instance of the Chrome (selenium.webdriver.Chrome).

        Returns:
            * None
        """
        self.chrome = chromeInstance

    def __del__(self):
        """
        Description:
            - Destructor method for the class.
        """

    def login(self, url: str, email: str) -> None:
        """
        Description:
            * Method to logs in to Magzter website using the provided URL and email.

        Args:
            * url (str):
                - The URL of the login page to log in to.
            * email (str):
                - The email address to use for logging in.

        Returns:
            * None
        """
        # Loading new page
        self.chrome.get(url)

        # 'Claim Now' button
        # self.chrome.find_element(By.TAG_NAME, "button").click()
        button: WebElement = scrap_tools.waitUntilElementLoadedInDOM(
            self.chrome, (By.TAG_NAME, "button")
        )
        button.click()

        # DOM is same and elements are present but focus page content changed. So, no need to use wait-until-load concept because already loaded.
        # Email input
        emailInputElement: WebElement = scrap_tools.waitUntilElementBecomeVisible(
            self.chrome, (By.NAME, "word")
        )
        emailInputElement.send_keys(email)
        self.chrome.find_element(By.CLASS_NAME, "login__loginBtnnp").click()

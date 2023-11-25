"""
    @file: components/microsoft.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 25th Nov 2023
    @error-series: 2300
    @description:
        * Module to perform any operations related to Microsoft for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utilities.scrap_tools import waitUntilElementLoaded


class Microsoft:
    """
    Description:
        - Class to perform operations related to Microsoft for the project.
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

    def login(self, url: str, email: str, password: str) -> None:
        """
        Description:
            * Method to logs in to Microsoft website using the provided URL, email, and password.

        Args:
            * url (str):
                - The URL of the login page to log in to.
            * email (str):
                - The email address to use for logging in.
            * password (str):
                - The password to use for logging in.

        Returns:
            * None
        """
        # Loading new page
        self.chrome.get(url)

        # self.chrome.find_element(By.ID, "i0116").send_keys(email)
        emailInputElement: WebElement = waitUntilElementLoaded(self.chrome, (By.ID, "i0116"))
        emailInputElement.send_keys(email)
        self.chrome.find_element(By.ID, "idSIButton9").click()

        # Page switched
        # self.chrome.find_element(By.ID, "i0118").send_keys(password)
        passwordInputElement: WebElement = waitUntilElementLoaded(self.chrome, (By.ID, "i0118"))
        passwordInputElement.send_keys(password)
        self.chrome.find_element(By.ID, "idSIButton9").click()

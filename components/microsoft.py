"""
    @file: components/microsoft.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 26th Nov 2023
    @error-series: 2300
    @description:
        * Module to perform any operations related to Microsoft for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utilities import scrap_tools


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

        # Input of email
        # self.chrome.find_element(By.ID, "i0116").send_keys(email)
        emailInputElement: WebElement = scrap_tools.waitUntilElementLoadedInDOM(
            self.chrome, (By.ID, "i0116")
        )
        emailInputElement.send_keys(email)
        self.chrome.find_element(By.ID, "idSIButton9").click()  # Clicking on next

        # DOM is same and elements are present but focus page content changed. So, no need to use wait-until-load concept because already loaded.
        # Input of password
        # self.chrome.find_element(By.ID, "i0118").send_keys(password)
        passwordInputElement: WebElement = scrap_tools.waitUntilElementBecomeVisible(
            self.chrome, (By.ID, "i0118")
        )
        passwordInputElement.send_keys(password)
        self.chrome.find_element(By.ID, "idSIButton9").click()  # clicking on next

    def openOutlook(self, url: str = "https://outlook.live.com/mail/0/") -> None:
        """
        Description:
            - Method to open the Outlook(mail) page in the chrome instance.
            - Must be called after login using Microsoft.login() method otherwise exception will be thrown.

        Args:
            * url (str):
                - The URL of the Outlook page to open.
                - Defaults to "https://outlook.live.com/mail/0/".

        Returns:
            * None
        """
        self.chrome.get(url)

        # A microsoft page open, having option to sign-in (We have already signed-in using login method. So, session is already there).
        # We just need to click on 'Sign in'

        # It opens a new tab for outlook because of target = _blank. We have update it using Javascript.
        # self.chrome.find_element(By.CSS_SELECTOR, 'a[data-bi-cn="SignIn"]')
        signInButton: WebElement = scrap_tools.waitUntilElementLoadedInDOM(
            self.chrome, (By.CSS_SELECTOR, 'a[data-bi-cn="SignIn"]')
        )
        # Changing target attribute value to '' using javascript. So, that outlook will open in same tab.
        self.chrome.execute_script(
            """document.querySelector('a[data-bi-cn="SignIn"]').target='';"""
        )
        signInButton.click()

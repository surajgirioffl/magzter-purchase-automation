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

    def writeOTP(self, otp: str) -> None:
        """
        Description:
            - Method to write OTP (One-Time Password) received from Magzter login.
            - It will write OTP to respective login page of the Magzter and press 'Verify' button.

        Args:
            * otp (str):
                - The OTP (One-Time Password) received from Magzter login.

        Returns:
            * None
        """
        # Writing OTP (4 digits)
        # self.chrome.find_element(By.ID, "otp1")

        # first cell of OTP (digit 1)
        scrap_tools.waitUntilElementLoadedInDOM(self.chrome, (By.ID, "otp1")).send_keys(otp[0])
        # 2nd cell of OTP (digit 2)
        self.chrome.find_element(By.ID, "otp2").send_keys(otp[1])
        # 3rd cell of OTP (digit 3)
        self.chrome.find_element(By.ID, "otp3").send_keys(otp[2])
        # 4th cell of OTP (digit 4)
        self.chrome.find_element(By.ID, "otp4").send_keys(otp[3])

        # clicking on verify button
        self.chrome.find_element(By.CLASS_NAME, "magzter__buttonText").click()

    def resendOTP(self) -> bool:
        """
        Description:
            - Method to resend the OTP for Magzter login.

        Returns:
            * bool:
                - True if the OTP is successfully resent, False otherwise.
                - Returns False if the current page is not Magzter login page.
        """
        # Magzter login page url is 'https://www.magzter.com/login/verify?from=&type=8'

        if not "login" in self.chrome.current_url:
            return False

        # 'logn__socialicons__signuplinks' class (<span>) should be clicked to resend OTP.
        scrap_tools.waitUntilElementBecomeClickable(
            self.chrome, (By.CLASS_NAME, "logn__socialicons__signuplinks")
        ).click()

        return True

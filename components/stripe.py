"""
    @file: components/microsoft.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 22nd Jan 2024
    @completed-on: N/A
    @last-modified: 22nd Jan 2024
    @error-series: 2500
    @description:
        * Module to perform any operations related to Stripe for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from time import sleep
from pyautogui import write, press
from utilities import scrap_tools
from selenium.webdriver import Chrome, Edge, Firefox
from selenium.webdriver.common.by import By


class Stripe:
    """
    Description:
        - Class to perform operations related to Stripe for the project.
    """

    def __init__(self, driverInstance: Chrome | Edge | Firefox) -> None:
        """
        Description:
            - Initializes a new instance of the class.

        Args:
            * driverInstance (Chrome | Edge | Firefox):
                - An instance of the any driver (selenium.webdriver.Chrome or any other).

        Returns:
            * None
        """
        self.driver = driverInstance

    def __del__(self):
        """
        Description:
            - Destructor method for the class.
        """

    def writeCardInformation(self, cardNumber: str, cardExpiry: str, cvc: str, cardholderName: str) -> None:
        """
        Description:
            - Method to writes the card information to the corresponding input boxes on the checkout page of Magzter and proceed.
                - Checkout page's URL is like https://checkout.stripe.com/c/pay/....

        Args:
            * cardNumber (str):
                - The card number to be entered.
            * cardExpiry (str):
                - The card expiry date to be entered.
            * cvc (str):
                - The cvc number to be entered.
            * cardholderName (str):
                - The name of the cardholder to be entered.

        Returns:
            * None
        """
        # card number input box: id = 'cardNumber'
        # self.driver.find_element(By.ID, "cardNumber").send_keys(cardNumber)
        scrap_tools.waitUntilElementLoadedInDOM(self.driver, (By.ID, "cardNumber")).send_keys(cardNumber)

        # card expiry input box: id = 'cardExpiry'
        self.driver.find_element(By.ID, "cardExpiry").send_keys(cardExpiry)

        # cvc input box: id = 'cardCvc'
        self.driver.find_element(By.ID, "cardCvc").send_keys(cvc)

        # card holder name input box: id = 'billingName'
        self.driver.find_element(By.ID, "billingName").send_keys(cardholderName)

        # country drop down: id = 'billingCountry' (default value is 'India') (No need to write)

        # pay button (div) class name: 'SubmitButton-IconContainer'
        self.driver.find_element(By.CLASS_NAME, "SubmitButton-IconContainer").click()

    def writeCardInformationLikeHuman(
        self,
        cardNumber: str,
        cardExpiry: str,
        cvc: str,
        cardholderName: str,
        sleepTimeOnEachEntry: float | int = 0,
    ) -> None:
        """
        Description:
            - Method to writes the card information to the corresponding input boxes on the checkout page of Magzter and proceed.
                - Checkout page's URL is like https://checkout.stripe.com/c/pay/....

        Args:
            * cardNumber (str):
                - The card number to be entered.
            * cardExpiry (str):
                - The card expiry date to be entered.
            * cvc (str):
                - The cvc number to be entered.
            * cardholderName (str):
                - The name of the cardholder to be entered.

        Returns:
            * None
        """
        press("tab", 3)
        sleep(sleepTimeOnEachEntry)
        write(cardNumber)
        sleep(sleepTimeOnEachEntry)
        press("tab")
        sleep(sleepTimeOnEachEntry)
        write(cardExpiry)
        sleep(sleepTimeOnEachEntry)
        press("tab")
        sleep(sleepTimeOnEachEntry)
        write(cvc)
        sleep(sleepTimeOnEachEntry)
        press("tab")
        sleep(sleepTimeOnEachEntry)
        write(cardholderName)
        sleep(sleepTimeOnEachEntry)
        press("tab", 3)
        sleep(sleepTimeOnEachEntry)
        press("enter")

    def isCorrectEmailOnPaymentPage(self, correctEmail: str) -> bool:
        """
        Description:
            - This function checks if the email entered on the payment page matches the correct email.

        Args:
            * correctEmail (str):
                - The correct email that should be on the payment page.

        Returns:
            * bool: True if the email on the payment page matches the correct email, False otherwise.
        """
        # "document.querySelector('.ReadOnlyFormField-title').innerText" give the readonly email from which the payment link belongs to.
        emailOnPaymentPage: str = scrap_tools.waitUntilElementLoadedInDOM(
            self.driver, (By.CSS_SELECTOR, ".ReadOnlyFormField-title")
        ).text.strip()
        return emailOnPaymentPage == correctEmail

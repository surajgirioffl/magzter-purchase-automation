"""
    @file: components/magzter.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 28th Nov 2023
    @error-series: 2400
    @description:
        * Module to perform any operations related to magzter for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

    def isOTPSuccessfullySubmitted(
        self, urlFragmentOfCheckoutPage: str = "checkout", maxWaitTimeForURLChange: int = 3
    ) -> bool | None:
        """
        Description:
            - Method to checks if OTP is successfully submitted.
            - Must be called after Magzter.writeOTP()

        Args:
            * urlFragmentOfCheckoutPage (str):
                - The URL fragment (any part of the URL) of the next page after OTP submission page which is checkout page.
                - Defaults to "checkout".
            * maxWaitTimeForURLChange (int):
                - The maximum wait time in seconds for the URL to change from OTP submission page to next page (checkout page).
                - Defaults to 3.

        Returns:
            * bool | None:
                - Returns True if OTP is successfully submitted,
                - False if not successfully submitted,
                - None if OTP is invalid and needs to be retried.
        """
        # How to check if OTP is successfully submitted
        # * Solution 1 (Using error message)
        # 'magazinename' class is a paragraph(<p>) containing error message if any error occurs.
        # It exist when an error occurs else not present in DOM.
        # It auto deleted from DOM when you rewrite the OTP or when no error.
        # Auto appears when an error occurs and disappears when you rewrite the OTP or when no error.
        # In case of invalid OTP: it contains 'Authentication failure'

        # * Solution 2 (Using changes in URL)
        # url during verification page (write otp page): https://www.magzter.com/login/verify?from=&type=8
        # On success it will redirect to one page and again auto redirect to checkout page: https://checkout.stripe.com/c/pay/cs_live_a1KRmUlrwPLqmy590zZjzQLi5CEO1UZQxRfo6DTWiwO46tMGPrmFdV8qeF#fidkdWxOYHwnPyd1blppbHNgWlIxSFR8Nl9gXXJQPWN8S3VSdnFPMVdmRCcpJ2hsYXYnP34nYnBsYSc%2FJ0tEJyknaHBsYSc%2FJ0tEJykndmxhJz8nS0QneCknZ2BxZHYnP15YKSdpZHxqcHFRfHVgJz8ndmxrYmlgWmxxYGgnKSd3YGNgd3dgd0p3bGJsayc%2FJ21xcXV2PyoqdWR8aGBrcStoZGJ%2FcWB3K2ZqaCd4JSUl
        # urlBeforeClickOnVerify: str = self.chrome.current_url
        # urlAfterClickOnVerify: str = self.chrome.current_url
        # return urlBeforeClickOnVerify != urlAfterClickOnVerify

        # **** Solving using both solution****
        # Checking if URL changes then success.
        try:
            scrap_tools.waitUntilCurrentURLContainsExpectedURLFragment(
                self.chrome, urlFragmentOfCheckoutPage, maxWaitTimeForURLChange
            )
        except TimeoutException as e:
            print(
                f"No URL changes found from OTP submission page to checkout page in last {maxWaitTimeForURLChange} seconds. Error Code: 2401"
            )
            print("Exception:", e)
            # Means URL did not change. So, it means OTP is not successfully submitted.
            # So, we will error para method to find exact reason.
            # If reason will invalid OTP then we will retry to fetch OTP from the outlook.
            # If url changes but again this exception occurs then increase maxWaitTimeForURLChange.
            pass
        else:
            # Success
            return True

        try:
            errorPara: WebElement = self.chrome.find_element(By.CLASS_NAME, "magazinename")
        except NoSuchElementException as e:
            return False
        else:
            errorText: str = errorPara.text
            print(f"OTP submission error: {errorText}. Error Code: 2402")
            if errorText.strip() == "Authentication failure":
                # Returns None if OTP is not successfully submitted due to invalid (wrong) OTP.
                # So, None will indicate to retry to fetch OTP from the outlook.
                return None
            return False

    def isOTPSuccessfullySubmitted_2(
        self, urlFragmentOfCheckoutPage: str = "checkout"
    ) -> bool | None:
        """
        Description:
            - Another Method to checks if OTP is successfully submitted.
            - Must be called after Magzter.writeOTP()

        Different from isOTPSuccessfullySubmitted():
            * This method is not bounded to wait time for URL changes.
            * It will check both error message and changes in URL in infinite loop.
            * Mainly developed to reduce time and increase performance of the application.
            * In previous method, control wait for URL changes and then check error message.
            * But it may possible error messages arose but URL not changes. So, wait time for URL changes is just waste of time.
            * So, better idea is to check both error message and changes in URL simultaneously in infinite loop to save unwanted time of waiting.

        Args:
            * urlFragmentOfCheckoutPage (str):
                - The URL fragment (any part of the URL) of the next page after OTP submission page which is checkout page.
                - Defaults to "checkout".

        Returns:
            * bool | None:
                - Returns True if OTP is successfully submitted,
                - False if not successfully submitted,
                - None if OTP is invalid and needs to be retried.
        """

        while True:
            # Checking for error message.
            try:
                errorPara: WebElement = self.chrome.find_element(By.CLASS_NAME, "magazinename")
            except NoSuchElementException as e:
                print("no error para found")
                pass
            else:
                errorText: str = errorPara.text
                print(f"OTP submission error: {errorText}. Error Code: 2403")
                if errorText.strip() == "Authentication failure":
                    # Returns None if OTP is not successfully submitted due to invalid (wrong) OTP.
                    # So, None will indicate to retry to fetch OTP from the outlook.
                    return None
                return False

            # checking for URL changes ( check for the URL fragment without waiting for any period)
            # * Bug:
            # Below try-except block cause stuck of the selenium. Selenium stuck and nothing happens, cursor in terminal blinks infinitely and browser got stuck.
            # This happens only after OTP submission successful and pages switched or are switching to next. Never happened if OTP is not successfully submitted.
            # When url is https://www.magzter.com/login/verify?from=&type=8 then no stuck happens and below try block executed.
            # But when URL switched or switching (which is only possible if OTP submission is success and this function is called for verification) then selenium stuck at this try block.
            # Reason: Abnormal behavior of stuck of selenium if expected_conditions.url_contains is used when url is changing and wait time is 0.
            # Frequency: The bug is not seen most of the time but not always.
            # So, as a workaround I made a manual check for the url fragment.

            try:
                scrap_tools.waitUntilCurrentURLContainsExpectedURLFragment_Manual(
                    self.chrome, urlFragmentOfCheckoutPage, 0.5
                )
            except TimeoutException as e:
                print("URL not match. Time out")
                pass
            else:
                print("Checkout page found")
                return True

    def writeCardInformation(
        self, cardNumber: str, cardExpiry: str, cvc: str, cardholderName: str
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
        # card number input box: id = 'cardNumber'
        # self.driver.find_element(By.ID, "cardNumber").send_keys(cardNumber)
        scrap_tools.waitUntilElementLoadedInDOM(self.chrome, (By.ID, "cardNumber")).send_keys(
            cardNumber
        )

        # card expiry input box: id = 'cardExpiry'
        self.chrome.find_element(By.ID, "cardExpiry").send_keys(cardExpiry)

        # cvc input box: id = 'cardCvc'
        self.chrome.find_element(By.ID, "cardCvc").send_keys(cvc)

        # card holder name input box: id = 'billingName'
        self.chrome.find_element(By.ID, "billingName").send_keys(cardholderName)

        # country drop down: id = 'billingCountry' (default value is 'India') (No need to write)

        # pay button (div) class name: 'SubmitButton-IconContainer'
        self.chrome.find_element(By.CLASS_NAME, "SubmitButton-IconContainer").click()

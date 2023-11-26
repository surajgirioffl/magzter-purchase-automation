"""
    @file: utilities/scrap_tools.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 25th Nov 2023
    @completed-on: N/A
    @last-modified: 26th Nov 2023
    @error-series: 3200
    @description:
        * Module to provide specific tools requires while performing scraping.
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome


def waitUntilElementLoadedInDOM(
    chromeInstance: Chrome, elementLocator: tuple, maxWaitTime: int = 10
) -> WebElement:
    """
    Description:
        - Function to wait until an element is loaded in a Chrome instance.

    Expectation:
        * presence_of_element_located
            - An expectation for checking that an element is present on the DOM of a page.
            - This does not necessarily mean that the element is visible.

    Args:
        * chromeInstance (Chrome):
            - The Chrome instance to wait on.
        * elementLocator (tuple):
            - The locator of the element to wait for.
                - Used to find the element returns the WebElement once it is located
            - E.g: (By.ID, "myElementId")
            - It must be a tuple.
        * maxWaitTime (int, optional):
            - The maximum time to wait for the element to be loaded, in seconds.
            - Defaults to 10.

    Returns:
        * WebElement:
            - The loaded element specified via the elementLocator.

    Raises:
        * selenium.common.exceptions.TimeoutException
            - If the element is not loaded within the specified time.
        * selenium.common.exceptions.NoSuchElementException
            - If the element is not found.
    """
    # Set a maximum wait time (in seconds)
    wait = WebDriverWait(chromeInstance, maxWaitTime)
    element: WebElement = wait.until(
        expected_conditions.presence_of_element_located(elementLocator)
    )
    return element


def waitUntilElementBecomeVisible(
    chromeInstance: Chrome, elementLocator: tuple, maxWaitTime: int = 10
) -> WebElement:
    """
    Description:
        - Function to wait until an element is visible in a Chrome instance.

    Expectation:
        * visibility_of_element_located
            - An expectation for checking that an element is present on the DOM of a page and visible.
            - Visibility means that the element is not only displayed but also has a height and width that is greater than 0.

    Args:
        * chromeInstance (Chrome):
            - The Chrome instance to wait on.
        * elementLocator (tuple):
            - The locator of the element to wait for.
                - Used to find the element returns the WebElement once it is located and visible
            - E.g: (By.ID, "myElementId")
            - It must be a tuple.
        * maxWaitTime (int, optional):
            - The maximum time to wait for the element to be visible, in seconds.
            - Defaults to 10.

    Returns:
        * WebElement:
            - The visible element specified via the elementLocator.

    Raises:
        * selenium.common.exceptions.TimeoutException
            - If the element is not loaded within the specified time.
        * selenium.common.exceptions.NoSuchElementException
            - If the element is not found.
    """
    # Set a maximum wait time (in seconds)
    wait = WebDriverWait(chromeInstance, maxWaitTime)
    element: WebElement = wait.until(
        expected_conditions.visibility_of_element_located(elementLocator)
    )
    return element


def waitUntilElementBecomeClickable(
    chromeInstance: Chrome, elementLocator: tuple, maxWaitTime: int = 10
) -> WebElement:
    """
    Description:
        - Function to wait until an element is visible and clickable in a Chrome instance.

    Expectation:
        * element_to_be_clickable
            - An Expectation for checking an element is visible and enabled such that you can click it.
            - Element is either a locator (text) or an WebElement.

    Args:
        * chromeInstance (Chrome):
            - The Chrome instance to wait on.
        * elementLocator (tuple):
            - The locator of the element to wait for.
                - Used to find the element returns the WebElement once it is located and clickable.
            - E.g: (By.ID, "myElementId")
            - It must be a tuple.
        * maxWaitTime (int, optional):
            - The maximum time to wait for the element to be visible, in seconds.
            - Defaults to 10.

    Returns:
        * WebElement:
            - The clickable element specified via the elementLocator.

    Raises:
        * selenium.common.exceptions.TimeoutException
            - If the element is not loaded within the specified time.
        * selenium.common.exceptions.NoSuchElementException
            - If the element is not found.
    """
    # Set a maximum wait time (in seconds)
    wait = WebDriverWait(chromeInstance, maxWaitTime)
    element: WebElement = wait.until(expected_conditions.element_to_be_clickable(elementLocator))
    return element


def waitUntilCurrentURLContainsExpectedURLFragment(
    chromeInstance: Chrome, expectedURLFragment: str, maxWaitTime: int = 5
) -> bool:
    """
    Description:
        - Function to wait until the current URL contains the expected URL fragment.
        - Means wait until URL changes to the URL contains the expected URL fragment.

    Expectation:
        - An expectation for checking that the current url contains a case- sensitive substring.

    Args:
        * chromeInstance (Chrome):
            - The Chrome instance to use for waiting.
        * expectedURLFragment (str):
            - The URL fragment(part) that is expected to be present in the current URL.
        * maxWaitTime (int, optional):
            - The maximum time to wait for the URL fragment to appear.
            - Defaults to 5.

    Returns:
        * bool:
            - True if the URL contains the expected fragment within the maximum wait time, False otherwise.
    """
    # Set a maximum wait time (in seconds)
    wait = WebDriverWait(chromeInstance, maxWaitTime)
    return wait.until(expected_conditions.url_contains(expectedURLFragment))


def waitUntilCurrentURLExactMatchToExpectedURL(
    chromeInstance: Chrome, expectedURL: str, maxWaitTime: int = 5
) -> bool:
    """
    Description:
        - Function to waits until the current URL matches the expected URL.
        - Means wait until URL changes to the URL exactly matches the expected URL.

    Expectation:
        - An expectation for checking the current url.

    Args:
        * chromeInstance (Chrome):
            - The instance of the Chrome browser.
        * expectedURL (str):
            - The URL that is expected to be matched.
        * maxWaitTime (int, optional):
            - The maximum wait time in seconds.
            - Defaults to 5.

    Returns:
        * bool:
            - True if the current URL matches the expected URL within the maximum wait time, False otherwise.
    """
    # Set a maximum wait time (in seconds)
    wait = WebDriverWait(chromeInstance, maxWaitTime)
    return wait.until(expected_conditions.url_to_be(expectedURL))


def openNewTab(chromeInstance: Chrome) -> None:
    """
    Description:
        - Function to open a new tab in the specified Chrome instance.

    Args:
        * chromeInstance (Chrome):
            - The Chrome instance to open the new tab in.

    Returns:
        * None
    """
    chromeInstance.execute_script("window.open('','_blank');")


def switchTab(chromeInstance: Chrome, tabIndex: int) -> None:
    """
    Description:
        - Function to switch the active tab of a Chrome instance to the tab at the specified index.

    Parameters:
        * chromeInstance (Chrome):
            - The Chrome instance.
        * tabIndex (int):
            - The index of the tab to switch to.
            - Index always starts from 0.
                - E.g: 1st tab has index 0, 2nd tab has index 1, and so on.

    Returns:
        None
    """
    chromeInstance._switch_to.window(chromeInstance.window_handles[tabIndex])

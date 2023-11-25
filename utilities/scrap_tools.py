"""
    @file: utilities/scrap_tools.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 25th Nov 2023
    @completed-on: N/A
    @last-modified: 25th Nov 2023
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

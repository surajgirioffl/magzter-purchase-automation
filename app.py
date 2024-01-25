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
    @last-modified: 25th Jan 2024
    @error-series: 1100
    @description:
        - Main module of the application (Driver module).
        - Python Version: 3.10.5
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "1.0.0"

from time import sleep, time
import logging
from sys import exit
from os.path import exists
from shutil import move
from os import remove
from datetime import datetime
from typing import Literal, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from components import ip, google_sheets, microsoft, magzter, stripe
from utilities import tools, scrap_tools
from db_scripts import spreadsheet_db

# Loading application settings
settings: dict = tools.loadAppSettings()
if not settings:
    # No settings found. Empty dictionary ({})
    print("No settings found. Error Code: 1101")
    tools.pressAnyKeyToContinue()
    exit(-1)

# Creating app required directories
tools.createAppRequiredDirectories(settings["app"]["required_directories"])


logging.basicConfig(
    filename="appdata/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(module)s:%(lineno)d - %(levelname)s -> %(message)s",
)


# Fetching URLs from settings
microsoftUrl: str = settings["url"]["microsoft"]
outlookUrl: str = settings["url"]["outlook"]
magzterUrl: str = settings["url"]["magzter"]


# Tab class to handling multiple tabs. It makes easy to switch between different tabs.
class Tab:
    Microsoft = 0
    Magzter = 1


# *************************************Spreadsheet Operations*************************************
def performInitialSpreadsheetOperations() -> tuple[str, str, google_sheets.GoogleSheets]:
    spreadSheetName: str | None = settings["spreadsheet"]["current"]["name"]
    sheetName: str | None = settings["spreadsheet"]["current"]["sheet_name"]

    def inputFromUserIfNone(name: str | None, title: str) -> str:
        if name is None:
            while True:
                name = input(f"Write {title} name: ")
                if name:
                    return name
                else:
                    print(f"Invalid {title} name.")
                    print("Write again...")
        return name

    spreadSheetName = inputFromUserIfNone(spreadSheetName, "spreadsheet")
    sheetName = inputFromUserIfNone(sheetName, "sheet")

    print(f"Fetching spreadsheet {spreadSheetName}...")
    gs = google_sheets.GoogleSheets(spreadSheetName, sheetTitleOrIndex=sheetName)

    print(f"Exporting spreadsheet to backups/{spreadSheetName}.xlsx if not exported earlier.")

    if exists(f"backups/{spreadSheetName}.xlsx"):
        print(
            f"Spreadsheet {spreadSheetName} is already exported earlier and exists in the backup directory."
        )
    else:
        print("Exporting...")
        print("It may take time as per size of spreadsheet and speed of internet connection.")
        if gs.exportSpreadsheet(f"backups/{spreadSheetName}.xlsx"):
            print("Spreadsheet exported successfully...")
        else:
            print("Something went wrong while exporting the spreadsheet. Error Code: 1102")

    return spreadSheetName, sheetName, gs


# ************************************Fetching RowNumber To Start************************************
def fetchRowNumberToStart(spreadSheetName: str, sheetName: str, lastSuccessStatFilePath: str):
    # Checking if current spreadsheet is used last time or not
    if exists(lastSuccessStatFilePath):
        # Resuming after last success row
        lastSuccessStat: dict = tools.loadLastSuccessStatistics(lastSuccessStatFilePath)
        if lastSuccessStat["spreadsheet"] == spreadSheetName and lastSuccessStat["sheet"] == sheetName:
            return int(lastSuccessStat["row"]) + 1
        else:
            print(
                "Conflict in spreadsheet name. Current spreadsheet name and spreadsheet name in last_success_stat_file don't match.  Error Code: 1103"
            )
            tools.pressAnyKeyToContinue()
            exit(-1)
    else:
        # Starting from scratch
        return settings["spreadsheet"]["data_start_row"]


class Menu:
    @staticmethod
    def confirmationMenu() -> None:
        print("=========================CONFIRMATION MENU=============================")
        print("Press 1 if Payment Successful.")
        print("Press 2 if Payment Failed.")


def confirmPaymentStatus() -> bool:
    while True:
        Menu.confirmationMenu()
        choice: str = input("Write your choice: ")
        if choice == "1":
            # Payment Success
            return True
        if choice == "2":
            # Payment Failed
            return False
        else:
            print("Invalid choice...")


def createLastSuccessStatJSONFile(
    spreadsheetName: str = None,
    sheetName: str = None,
    ip: str = None,
    row: int = 2,
    dateTime: str = str(datetime.today()),
    lastSuccessStatFilePath: str = "appdata/last_success_statistics.json",
) -> None:
    # As per format of the last_success_stat_file.
    data = {
        "spreadsheet": spreadsheetName,
        "sheet": sheetName,
        "ip": ip,
        "row": row,
        "date_time": dateTime,
    }
    tools.saveDictAsJSON(data, lastSuccessStatFilePath)


def getUniqueIPAddress(spreadsheetDb: spreadsheet_db.Spreadsheet) -> str:
    while True:
        print("Fetching your current IP address...")
        currentIP: str = ip.getCurrentIP()
        if currentIP:
            print(f"Your current IP address: {currentIP}")
            # Checking if IP exits or not
            if spreadsheetDb.isIpExists(currentIP):
                print("IP already exists in the current sheet.")
                print("Please change your IP..")
            else:
                return currentIP
        else:
            print("Invalid IP address. Please try again...")

        tools.pressAnyKeyToContinue("\nPress any key to continue to check again.")


class NewDriverInstance:
    @staticmethod
    def getNewChromeInstance():
        # Options and services must be initialized for each browser session because when you quit a browser then these objects are also destroyed.
        # Adding chrome options based on user settings
        chromeOptions = webdriver.chrome.options.Options()
        if not settings["browser"]["display_images"]:
            chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
        if settings["browser"]["headless"]:
            chromeOptions.add_argument("--headless")

        # Services
        service = Service(
            executable_path=settings["webdriver"]["executable_path"],
            port=settings["webdriver"]["port"],
        )
        return webdriver.Chrome(options=chromeOptions, service=service)

    @staticmethod
    def getNewEdgeInstance():
        # Options and services must be initialized for each browser session because when you quit a browser then these objects are also destroyed.
        # Adding edge options based on user settings
        edgeOptions = webdriver.edge.options.Options()
        if not settings["browser"]["display_images"]:
            edgeOptions.add_argument("--blink-settings=imagesEnabled=false")
        if settings["browser"]["headless"]:
            edgeOptions.add_argument("--headless")

        # Services
        service = Service(
            executable_path=settings["webdriver"]["executable_path"],
            port=settings["webdriver"]["port"],
        )
        return webdriver.Edge(options=edgeOptions, service=service)

    @staticmethod
    def getNewFirefoxInstance():
        # Options and services must be initialized for each browser session because when you quit a browser then these objects are also destroyed.
        # Adding firefox options based on user settings
        firefoxOptions = webdriver.firefox.options.Options()
        if not settings["browser"]["display_images"]:
            firefoxOptions.set_preference("permissions.default.image", 2)
        if settings["browser"]["headless"]:
            firefoxOptions.add_argument("--headless")

        # Services
        service = Service(
            executable_path=settings["webdriver"]["executable_path"],
            port=settings["webdriver"]["port"],
        )
        return webdriver.Firefox(options=firefoxOptions, service=service)


class NewUndetectableDriverInstance:
    @staticmethod
    def getNewChromeInstance():
        chromeOptions = webdriver.chrome.options.Options()
        if not settings["browser"]["display_images"]:
            chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
        if settings["browser"]["headless"]:
            chromeOptions.add_argument("--headless")

        # Services
        service = Service(
            executable_path=settings["webdriver"]["executable_path"],
            port=settings["webdriver"]["port"],
        )
        return uc.Chrome(options=chromeOptions, service=service)


def main() -> None:
    # *********************************Scraping Objects & Variables*********************************
    spreadSheetName, sheetName, gs = performInitialSpreadsheetOperations()  # gs is a GoogleSheets object

    lastSuccessStatFilePath: str = settings["app"]["last_success_stat_file"]
    headersWithIndex: dict = settings["spreadsheet"]["headers_with_index"]
    headersWithColumn: dict = settings["spreadsheet"]["headers_with_column"]

    spreadsheetDb = spreadsheet_db.Spreadsheet(spreadSheetName, sheetName)

    # Scraping Starts
    # *************************************Scraping Starts*************************************

    # TODO -> Fetching desired row number to start and data of the respective row from the Google sheet
    rowNumber: int = fetchRowNumberToStart(spreadSheetName, sheetName, lastSuccessStatFilePath)
    index = 0

    while True:
        iterationStartTime: float = time()
        # Options and services must be initialized for each browser session because when you quit a browser then these objects are also destroyed.
        # New browser session (Because clear cookies is not working for microsoft)
        # Initializing the chrome webdriver
        print("\nInitializing a new browser session...")
        driver: webdriver.Firefox = NewDriverInstance.getNewFirefoxInstance()
        print("Browser session initialized successfully...")

        # Initializing the objects of Microsoft and Magzter
        ms: microsoft.Microsoft = microsoft.Microsoft(driver)
        mg: magzter.Magzter = magzter.Magzter(driver)

        print(f"\n\n======================== FOR ROW NUMBER {rowNumber} ========================")
        # TODO -> Checking IP
        print("Fetching your current IP address...")
        currentIP = getUniqueIPAddress(spreadsheetDb)

        print(f"Fetching contents of row number {rowNumber}...")
        rowData: list = gs.getRowValues(rowNumber)
        if not rowData:
            # If the row is empty. Means all rows have been fetched.
            # Complete the transaction and exit.
            move(lastSuccessStatFilePath, "appdata/history/last-success-statics/")
            print(
                f"Scraping and manipulation of sheet {sheetName} of Spreadsheet {spreadSheetName} completed successfully..."
            )
            print("Last success stat file removed successfully...")
            break

        print(f"Fetched row data: {rowData}")

        # TODO -> Login to Microsoft and open outlook
        # Microsoft in tab index 0
        print("Login to Microsoft and open Outlook...")
        email: str = rowData[headersWithIndex["microsoft_email"]]
        password: str = rowData[headersWithIndex["password"]]
        scrap_tools.switchTab(driver, Tab.Microsoft)
        ms.login(microsoftUrl, email, password)
        ms.openOutlook(outlookUrl)

        # TODO -> Login to Magzter till send OTP
        # Opening new tab for Magzter
        scrap_tools.openNewTab(driver)
        # Magzter in tab index 1
        print("Login to Magzter and send OTP...")
        scrap_tools.switchTab(driver, Tab.Magzter)
        mg.login(magzterUrl, email)  # OTP sent

        # TODO -> Fetching and writing OTP
        print("Fetching and writing OTP...")
        while True:
            print("-- Fetching and Writing OTP")
            # Fetching OTP from microsoft tab
            scrap_tools.switchTab(driver, Tab.Microsoft)
            otp: str = ms.fetchOTP()
            print("otp: ", otp)
            if not otp.strip():
                print("OTP is empty. Retrying to fetch OTP...")
                continue

            # Writing OTP to magzter tab
            scrap_tools.switchTab(driver, Tab.Magzter)
            mg.writeOTP(otp)
            sleep(1)  # sleep for 1 second

            status: bool | None = mg.isOTPSuccessfullySubmitted(maxWaitTimeForURLChange=5)  # Time consuming.
            print("OTP fetch status:", status)

            if status:
                # OTP successfully submitted. So, break the loop.
                print("OTP successfully submitted..")
                break
            elif status is None:
                # Invalid OTP. So, retry to fetch OTP.
                print("Invalid OTP. Retrying to fetch OTP...")
                continue
            else:
                # Some other error. So, switch the control to user.
                otpByUser = input("Write OTP: ")
                # Writing OTP to magzter tab
                mg.writeOTP(otpByUser)
                break

        paymentPageLink: str = driver.current_url
        # TODO -> Fetching and writing card information (Stripe page works)
        print("Fetching and writing card information...")
        cardNumber: str = rowData[headersWithIndex["card_number"]]
        cardExpiry: str = rowData[headersWithIndex["card_expiry"]]
        cardCvv: str = rowData[headersWithIndex["card_cvv"]]
        cardholderName: str = rowData[headersWithIndex["cardholder_name"]]

        uDriver = NewUndetectableDriverInstance.getNewChromeInstance()
        uDriver.get(paymentPageLink)
        stp = stripe.Stripe(uDriver)
        sleep(3)
        if not stp.isCorrectEmailOnPaymentPage():
            print("Email on the page is not same as the email logged in.")
            print("Something went wrong.. Error Code: ")
            print("Please don't proceed. Close the application...")
            input("Press enter to continue (Not recommended): ")

        stp.writeCardInformation(cardNumber, cardExpiry, cardCvv, cardholderName)
        print("Card Information written..")

        print("Writing reference IDs...")
        corporateId: str = rowData[headersWithIndex["corporate"]]
        employeeId: str = rowData[headersWithIndex["employee_id"]]
        stp.writeUniqueReferenceIDLikeHuman(corporateId, employeeId)
        print("If reference IDs are not written then copy and paste from here..")
        print(f"Corporate ID: {corporateId}")
        print(f"Employee ID: {employeeId}")
        print("done...")

        print("\n")
        print(f"Time taken till this point for row {rowNumber} is {time()-iterationStartTime:.2f} seconds.")
        print("\n")
        paymentStatus = confirmPaymentStatus()
        paymentStatus = "Success" if paymentStatus else "Failed"

        # TODO -> Updating the current row of google sheet with new desired information
        print("Updating the current row of google sheet with new desired information")
        cellValueDict: dict = {
            f"{headersWithColumn['ip']}{rowNumber}": currentIP,
            f"{headersWithColumn['ip_same_check']}{rowNumber}": "False",
            f"{headersWithColumn['status']}{rowNumber}": paymentStatus,
        }
        gs.updateMultipleCells(cellValueDict)

        # TODO -> Updating the last success stat file
        createLastSuccessStatJSONFile(
            spreadSheetName, sheetName, currentIP, rowNumber, lastSuccessStatFilePath=lastSuccessStatFilePath
        )

        # TODO -> Inserting the current ip to the database.
        print("Inserting the current ip to the database...")
        spreadsheetDb.insertIp(currentIP)

        iterationEndTime: float = time()
        print(f"Total time for row {rowNumber} is {iterationEndTime-iterationStartTime:.2f} seconds.")

        # Updating the row number and index
        rowNumber += 1  # incrementing the row number
        index += 1

        # Closing the browser
        print("Closing both browsers till then please change your IP.")
        # Ensure that chrome.quit() is called regardless of what happens.
        driver.quit()
        uDriver.quit()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Something went wrong while automating the stuffs. Error Code: 1104")
            print("Exception:", e)

            print("\nPress enter to try again or '#' to exit.")
            if input() == "#":
                input("Press Enter to exit...")
                exit(-1)
            else:
                print("Trying again...")
                continue
        else:
            print("Process completed...\n")
            input("Press Enter to exit...")

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
    @last-modified: 30th Nov 2023
    @error-series: 1100
    @description:
        - Main module of the application (Driver module).
        - Python Version: 3.10.5
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"
__version__ = "1.0.0"

from time import sleep
from warnings import filterwarnings
from sys import exit
from os.path import exists
from shutil import move
from os import remove
from datetime import datetime
from typing import Literal, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from components import ip, google_sheets, microsoft, magzter
from utilities import tools, scrap_tools
from db_scripts import spreadsheet_db

# Filter warnings
filterwarnings("ignore")

# Loading application settings
settings: dict = tools.loadAppSettings()
if not settings:
    # No settings found. Empty dictionary ({})
    print("No settings found. Error Code: 1101")
    tools.pressAnyKeyToContinue()
    exit(-1)

# Creating app required directories
tools.createAppRequiredDirectories(settings["app"]["required_directories"])

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
        # Options and services must be initialized for each browser session because when you quit a browser then these objects are also destroyed.

        # Adding chrome options based on user settings
        chromeOptions: Options = Options()
        if not settings["chrome"]["display_images"]:
            chromeOptions.add_argument("--blink-settings=imagesEnabled=false")
        if settings["chrome"]["headless"]:
            chromeOptions.add_argument("--headless")

        # Services
        service = Service(
            executable_path=settings["chromedriver"]["executable_path"],
            port=settings["chromedriver"]["port"],
        )

        # New browser session (Because clear cookies is not working for microsoft)
        # Initializing the chrome webdriver
        print("\nInitializing a new browser session...")
        chrome: webdriver.Chrome = webdriver.Chrome(options=chromeOptions, service=service)

        # Initializing the objects of Microsoft and Magzter
        ms: microsoft.Microsoft = microsoft.Microsoft(chrome)
        mg: magzter.Magzter = magzter.Magzter(chrome)

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
        scrap_tools.switchTab(chrome, Tab.Microsoft)
        ms.login(microsoftUrl, email, password)
        ms.openOutlook(outlookUrl)

        # TODO -> Login to Magzter till send OTP
        # Opening new tab for Magzter
        scrap_tools.openNewTab(chrome)
        # Magzter in tab index 1
        print("Login to Magzter and send OTP...")
        scrap_tools.switchTab(chrome, Tab.Magzter)
        mg.login(magzterUrl, email)  # OTP sent

        # TODO -> Fetching and writing OTP
        print("Fetching and writing OTP...")
        while True:
            print("-- Fetching and Writing OTP")
            # Fetching OTP from microsoft tab
            scrap_tools.switchTab(chrome, Tab.Microsoft)
            otp: str = ms.fetchOTP()
            print("otp: ", otp)
            if not otp.strip():
                print("OTP is empty. Retrying to fetch OTP...")
                continue

            # Writing OTP to magzter tab
            scrap_tools.switchTab(chrome, Tab.Magzter)
            mg.writeOTP(otp)

            # status: bool | None = mg.isOTPSuccessfullySubmitted(maxWaitTimeForURLChange=5) # Time consuming.
            status: bool | None = mg.isOTPSuccessfullySubmitted_2()
            print("Returned from isOTPSuccessfullySubmitted_2")
            print("status:", status)

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
                mg.writeOTP(otp)
                break

        # TODO -> Fetching and writing card information
        print("Fetching and writing card information...")
        carNumber: str = rowData[headersWithIndex["card_number"]]
        cardExpiry: str = rowData[headersWithIndex["card_expiry"]]
        cardCvv: str = rowData[headersWithIndex["card_cvv"]]
        cardholderName: str = rowData[headersWithIndex["cardholder_name"]]
        mg.writeCardInformation(carNumber, cardExpiry, cardCvv, cardholderName)

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

        # Updating the row number and index
        rowNumber += 1  # incrementing the row number
        index += 1

        # Closing the browser
        print("Closing the browser..")
        # Ensure that chrome.quit() is called regardless of what happens.
        if "chrome" in locals() and hasattr(chrome, "quit"):
            chrome.quit()


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

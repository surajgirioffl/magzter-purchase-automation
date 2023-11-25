"""
    @file: components/google_sheets.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 25th Nov 2023
    @error-series: 2200
    @description:
        * Module to perform any operation related to the Google Sheets required for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

from typing import Literal
from sys import exit
import gspread
from gspread.utils import ExportFormat


class GoogleSheets:
    """
    Description:
        - Class to perform any operation related to the Google Sheets required for the project.
    """

    def __init__(
        self,
        ValueOfOpenSpreadsheetBy: str,
        openSpreadsheetBy: Literal["name", "url", "id"] = "name",
        sheetTitleOrIndex: str | int = 0,
        googlCredentialsJSONPath: str = "google-secrets.json",
        exitOnError: bool = True,
    ) -> None:
        """
        Description:
            - Constructor of the GoogleSheets class.
            - Initializes the GoogleSheets object to perform different operations related to the Google Sheets required for the project.

        Parameters:
            * ValueOfOpenSpreadsheetBy (str):
                - The value used to open the spreadsheet.
                - It is value specified in the argument 'openSpreadSheetBy' (next argument).
                - In default, provide name of the spreadsheet to open.
            * openSpreadsheetBy (Literal["name", "url", "id"], optional):
                - The method used to open the spreadsheet.
                - Defaults to "name".
            * sheetTitleOrIndex (str | int, optional):
                - The title or index of the worksheet to open.
                - Defaults to 0.
                - Integer or numeric string will treated as index and string will treated as title.
            * googlCredentialsJSONPath (str, optional):
                - The path to the JSON file containing the Google Sheets credentials.
                - Defaults to "google-secrets.json" (in the root directory of the project).
            * exitOnError (bool, optional):
                - Whether to exit the program if an error occurs.
                - Defaults to True.
                - If set to False then further you will get abnormal termination of the program.

        * Returns:
            - None

        * Exit:
            * Exit: If there is an error while connecting to Google Sheets or fetching the spreadsheet or worksheet.
        """
        try:
            self.client = gspread.service_account(filename=googlCredentialsJSONPath)
        except Exception as e:
            print(
                "Something went wrong while connecting to Google Sheets (May be credentials file not found). Error Code: 2201"
            )
            print("Exception:", e)
            exit(-1) if exitOnError else None

        # Opening the desired spreadsheet
        try:
            if openSpreadsheetBy == "name":
                self.spreadsheet = self.client.open(ValueOfOpenSpreadsheetBy)
            elif openSpreadsheetBy == "url":
                self.spreadsheet = self.client.open_by_url(ValueOfOpenSpreadsheetBy)
            elif openSpreadsheetBy == "id":
                self.spreadsheet = self.client.open_by_key(ValueOfOpenSpreadsheetBy)
        except Exception as e:
            print(
                "Something went wrong while fetching the spreadsheet. Error Code: 2202"
            )
            print("Exception:", e)
            exit(-1) if exitOnError else None

        # Opening the desired worksheet
        try:
            if isinstance(sheetTitleOrIndex, int) or sheetTitleOrIndex.isnumeric():
                self.worksheet = self.spreadsheet.get_worksheet(sheetTitleOrIndex)
            else:
                self.worksheet = self.spreadsheet.worksheet(sheetTitleOrIndex)
        except Exception as e:
            print("Something went wrong while fetching the worksheet. Error Code: 2203")
            print("Exception:", e)
            exit(-1) if exitOnError else None

    def __del__(self):
        """
        Description:
            - Destructor method for the class.
        """

    def exportSpreadsheet(
        self,
        filenameOrPathWithExtension: str,
        exportFormat: Literal[
            "PDF", "EXCEL", "CSV", "OPEN_OFFICE_SHEET", "TSV", "ZIPPED_HTML"
        ] = "EXCEL",
    ) -> bool:
        """
        Description:
            - Function to exports the spreadsheet to the specified file in the given format.

        Args:
            * filenameOrPathWithExtension (str):
                - The name or path of the file to export the spreadsheet to, including the file extension.
            * exportFormat (Literal["PDF", "EXCEL", "CSV", "OPEN_OFFICE_SHEET", "TSV", "ZIPPED_HTML"], optional):
                - The format in which to export the spreadsheet.
                - The format may be any one from the following list: "PDF", "EXCEL", "CSV", "OPEN_OFFICE_SHEET", "TSV", "ZIPPED_HTML".
                - Defaults to "EXCEL".

        Returns:
            * bool:
                - True if the export was successful, False otherwise.
        """
        contents: bytes = self.spreadsheet.export(getattr(ExportFormat, exportFormat))
        try:
            with open(filenameOrPathWithExtension, "wb") as file:
                file.write(contents)
        except Exception as e:
            print(
                "Something went wrong while exporting the spreadsheet. Error Code: 2204"
            )
            print("Exception:", e)
            return False
        else:
            return True

    def getRowValues(self, rowIndex: int) -> list:
        """
        Description:
            - Method to retrieves the values of a specific row in the worksheet.

        Args:
            * rowIndex (int):
                - The index of the row to retrieve values from.

        Returns:
            * list: 
                - A list containing the values of the specified row.
                - Return empty list([]) if the row does not exist.
        """
        return self.worksheet.row_values(rowIndex)

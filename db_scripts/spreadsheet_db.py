"""
    @file: db_scripts/spreadsheet_db.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 29th Nov 2023
    @error-series: 4200
    @description:
        - Module to handle database related operations on spreadsheet.
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

import sqlite3 as sqlite
from db_scripts import schema


class Spreadsheet:
    """
    @description:
        - Class to handle database related operations on spreadsheet.
    """

    def __init__(self, databaseName: str, tableName: str, path: str = "appdata/databases") -> None:
        """
        Description:
            - Constructor to instantiate Spreadsheet object.

        Args:
            * databaseName(str):
                - Name of the database to connect.
                - It will same as the name of the spreadsheet.
            * tableName(str):
                - Table name to be created if not exits.
                - It will same as the name of the sheet.
            * path(str):
                - Path to store/fetch the database.
                - Defaults to 'appdata/databases'
        Returns:
            * None
        """
        try:
            self.conn = sqlite.connect(f"{path}/{databaseName}.db")
            self.cursor = self.conn.cursor()
            self.connectionStatus = True
            self.tableName = tableName
            self.databaseName = databaseName
        except Exception as e:
            print("Connection failed. Error code 4201")
            print("Exception:", e)
            # To check if connection is established or not.
            self.connectionStatus = False
        else:
            try:
                self.cursor.execute(schema.Spreadsheet.getIPTableSchema(tableName))
                self.conn.commit()
            except Exception as e:
                print(f"Unable to create table {tableName}. Error Code: 4202")
                print("Exception:", e)

    def __del__(self) -> None:
        """
        @description:
            - Destructor to destroy the instance.
        """
        if self.connectionStatus:
            self.conn.commit()
            self.conn.close()

    def isIpExists(self, ip: str) -> bool:
        """
        Description:
            - Method to check if the given IP address exists in the specified sheet(table) of the database(spreadsheet).

        Parameters:
            * ip (str):
                - The IP address to be checked.

        * Returns:
            * bool:
                - True if the IP address exists in the table, False otherwise.
        """
        try:
            self.cursor.execute(
                f"""-- sql
                    SELECT * FROM `{self.tableName}`
                    WHERE ip = '{ip}'
                """
            )
        except Exception as e:
            print("Something went wrong while checking if IP exists. Error Code: 4203")
            print("Exception: ", e)
        else:
            return self.cursor.fetchone() is not None

    def insertIp(self, ip: str) -> None:
        """"""
        """
        Description:
            - Method to insert an IP address into the database.

        Args:
            *ip (str):
                - The IP address to insert.

        Returns:
            * None:
                - This function does not return anything.

        Raises:
            * Exception: If there is an error while inserting the IP address.
        """
        try:
            self.cursor.execute(
                f"""-- sql
                    INSERT INTO `{self.tableName}` (ip)
                    VALUES('{ip}')
                """
            )
        except Exception as e:
            print("Something went wrong while inserting IP. Error Code: 4204")
            print("Exception: ", e)
            raise e.__class__(e)
        else:
            self.conn.commit()


if __name__ == "__main__":
    spreadsheet = Spreadsheet("test", "temp")
    print(spreadsheet.isIpExists("127.9.61.92"))
    print(spreadsheet.isIpExists("128.9.61.93"))
    spreadsheet.insertIp("128.9.61.93")

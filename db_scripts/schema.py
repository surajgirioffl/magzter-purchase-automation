"""
    @file: db_scripts/schema.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 29th Nov 2023
    @completed-on: N/A
    @last-modified: 29th Nov 2023
    @error-series: 4100
    @description:
            - Module containing schema for tables of databases(classname).
"""
__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"


class Spreadsheet:
    @staticmethod
    def getIPTableSchema(tableName: str) -> str:
        schema: str = f"""-- sql
                        CREATE TABLE IF NOT EXISTS `{tableName}`
                        (
                            `ip` VARCHAR(50) PRIMARY KEY NOT NULL,
                            `inserted_at` DATETIME NOT NULL DEFAULT (DATETIME('now', 'localtime'))
                        );
                    """
        return schema

"""
    @file: app_scripts/tools.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 24th Nov 2023
    @error-series: 3100
    @description:
        * Module to perform any extra operations required for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

import os


def createAppRequiredDirectories(
    directoriesWithPath: list | tuple | set = {"appdata"},
) -> None:
    """
    Description:
        - Function to create all required directories of the application.

    Args:
        * directoriesWithPath (list | tuple | set, optional):
                - List of directories to create.
                    - You can specify multiple directories along with paths.
                    - If no path provided then it will taken as current working directory (root directory of the project/application)
                    - You can also provided hierarchical directories path, all directories of the hierarchy will be created.
                - Defaults to {"appdata"}.
    Returns:
        * None
    """
    try:
        for directory in directoriesWithPath:
            os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print("Unable to create directories problems/language1,2.. Error Code: 3101")
        print("Exception:", e)


if __name__ == "__main__":
    createAppRequiredDirectories()

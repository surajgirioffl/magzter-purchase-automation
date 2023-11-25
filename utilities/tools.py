"""
    @file: utilities/tools.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 25th Nov 2023
    @error-series: 3100
    @description:
        * Module to perform any extra operations required for the project.
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

import os
import json


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
        print(f"Unable to create the directory '{directory}'. Error Code: 3101")
        print("Exception:", e)


def loadJSONFile(filePath: str = "settings.json") -> dict | list:
    """
    Description:
        - Function to load JSON file specified in the parameter.
        - The function reads the JSON data and returns it as a dictionary or list (as per JSON).

    Args:
        * filePath (str, optional):
            - Path to the desired JSON file.
            - Defaults to "settings.json".

    Returns:
        * dict:
            - Return a dictionary or list containing JSON data on success else an empty dictionary.
                - Dictionary if JSON will like {...}
                - List if JSON will like [...]
                - Empty dictionary if JSON file is not found or any error or exception occurs.
    """
    try:
        with open(filePath, "r") as jsonFile:
            jsonData: dict = json.load(jsonFile)
    except Exception as e:
        print(f"Unable to open the file {filePath}. Error Code: 3102")
        print("Exception:", e)
        return {}
    else:
        print(f"{filePath} file loaded successfully...")
        return jsonData


def saveDictAsJSON(
    dictData: dict, fileNameOrPathWithExtension: str, mode="w", indent=2
) -> bool:
    """
    Description:
        - Function to Save a dictionary as JSON.

    Parameters:
        * dictData (dict):
            - The dictionary to be saved as JSON.
        * fileNameOrPathWithExtension (str):
            - The name or path of the file where the JSON will be saved (with 'json' extension)
        * mode (str, optional):
            - The file mode to open the file in.
            - Defaults to "w".
        * indent (int, optional):
            - The number of spaces to use for indentation in the JSON.
            - Defaults to 2.

    Returns:
        * bool:
            - True if the dictionary was successfully saved as JSON, False otherwise.
    """
    try:
        jsonData = json.dumps(dictData, indent=indent)
        with open(fileNameOrPathWithExtension, mode) as jsonFile:
            jsonFile.write(jsonData)
    except Exception as e:
        print("Unable to save dictionary as JSON. Error Code: 3103")
        print("Exception:", e)
        return False
    else:
        return True


def loadAppSettings(settingsFilePath: str = "settings.json") -> dict:
    """
    Description:
        - Function to load application settings and configurations stored in a 'settings.json' file.
        - The function reads the JSON data and returns it as a dictionary

    Args:
        * settingsFilePath (str, optional):
            - Path to the settings.json file (Name may be different)
            - Defaults to "settings.json".

    Returns:
        * dict:
            - Return a dictionary containing settings configuration on success else an empty dictionary.
    """
    return loadJSONFile(settingsFilePath)


def loadAppSecrets(secretFilePath: str = "secrets.json") -> dict:
    """
    Description:
        - Function to load application secrets stored in a 'secrets.json' file.
        - The function reads the JSON data and returns it as a dictionary

    Args:
        * settingsFilePath (str, optional):
            - Path to the secrets.json file (Name may be different)
            - Defaults to "secrets.json".

    Returns:
        * dict:
            - Return a dictionary containing application secrets on success else an empty dictionary.
    """
    return loadJSONFile(secretFilePath)


def loadLastSuccessStatistics(
    statisticsFilePath: str = "appdata/last_success_statistics.json",
) -> dict:
    """
    Description:
        - Function to load last successful operation statistics stored in a 'appdata/last_success_statistics.json' file.
        - The function reads the JSON data and returns it as a dictionary

    Args:
        * settingsFilePath (str, optional):
            - Path to the last_success_statistics.json file (Name may be different)
            - Defaults to "appdata/last_success_statistics.json".

    Returns:
        * dict:
            - Return a dictionary containing last successful operation statistics on success else an empty dictionary.
    """
    return loadJSONFile(statisticsFilePath)


if __name__ == "__main__":
    createAppRequiredDirectories()
    saveDictAsJSON({"key": None}, "test.json")

"""
    @file: components/ip.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 30th Nov 2023
    @error-series: 2100
    @description:
        * Module to perform any operations related to IP for the project including fetching the current IP, IP comparison and more..
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

import requests


def getCurrentIP(sourceAPIEndpoint: str = "https://api.bigdatacloud.net/data/client-ip") -> str:
    """
    Description:
        - Function to fetch the current IP from the specified API.

    Args:
        * sourceAPIEndpoint (str, optional):
            - API endpoint to fetch the current IP.
            - Defaults to "https://api.bigdatacloud.net/data/client-ip".

    Returns:
        * str:
            - Return the current IP on success else an empty string.

    Future:
        - In future, we can add functionality to use API credentials, if required.
        - Currently, as per project need, we don't need any credentials.
    """
    try:
        response = requests.get(sourceAPIEndpoint)
    except Exception as e:
        print("Something went wrong while fetching current IP. Error Code: 2101")
        print("Exception:", e)
        return ""
    else:
        if response.status_code == 200:
            return response.json()['ipString']
        else:
            print("Something went wrong while fetching current IP. Error Code: 2102")
            print("Status Code:", response.status_code)
            return ""


def compareIPs(
    currentIP: str,
    lastIP: str = None,
    readLastIpFromFile: bool = True,
    filePath: str = "appdata/last-ip.txt",
    returnTrueIfFileNotFound: bool = True,
) -> bool:
    """
    Description:
        - Compare two IP addresses and return a boolean value indicating whether they are equal.

    Args:
        * currentIP (str):
            - The IP address to compare.
        * lastIP (str, optional):
            - The last IP address to compare.
            - If it will be given then none of next parameters will be used. It has max priority.
            - Defaults to None.
        * readLastIpFromFile (bool, optional):
            - Whether to read the last IP address from a file.
            - Defaults to True.
        * filePath (str, optional):
            - The path to the file containing the last IP address.
            - Defaults to "appdata/last-ip.txt".
        * returnTrueIfFileNotFound (bool, optional):
            - Whether to return True if the file is not found.
            - True is better in case file is not yet created.
            - Defaults to True.

    Returns:
        * bool:
            - True if the IP addresses are equal, False otherwise.
    """
    if readLastIpFromFile and lastIP is None:
        try:
            with open(filePath) as file:
                lastIP: str = file.read()
            lastIP: str = lastIP.strip()
        except FileNotFoundError as e:
            if returnTrueIfFileNotFound:
                return True
            print(f"File '{filePath}' not found. Error Code: 2103")
            print("Exception:", e)
            return False
        except Exception as e:
            print(
                f"Something went wrong while reading last IP from the file. Error Code: 2104"
            )
            print("Exception:", e)
            return False
        else:
            return True if currentIP == lastIP else False

    return True if currentIP == lastIP else False


if __name__ == "__main__":
    print(getCurrentIP())
    print(compareIPs("127.0.0.1"))

"""
    @file: components/ip.py
    @author: Suraj Kumar Giri (https://github.com/surajgirioffl)
    @init-date: 24th Nov 2023
    @completed-on: N/A
    @last-modified: 24th Nov 2023
    @error-series: 2100
    @description:
        * Module to perform any operations related to IP for the project including fetching the current IP, IP comparison and more..
"""

__author__ = "Suraj Kumar Giri"
__email__ = "surajgirioffl@gmail.com"

import requests


def getCurrentIP(sourceAPIEndpoint: str = "https://api.ipify.org/") -> str:
    """
    Description:
        - Function to fetch the current IP from the specified API.

    Args:
        * sourceAPIEndpoint (str, optional):
            - API endpoint to fetch the current IP.
            - Defaults to "https://api.ipify.org/".

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
    else:
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("Something went wrong while fetching current IP. Error Code: 2102")
            print("Status Code:", response.status_code)
            return ""


if __name__ == "__main__":
    print(getCurrentIP())

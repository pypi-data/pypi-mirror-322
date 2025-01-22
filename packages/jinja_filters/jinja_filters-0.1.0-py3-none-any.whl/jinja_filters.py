"""
This module provides filters that can be used for jinja2 formatting.
"""

from datetime import datetime

def format_date(input_date: datetime):
    return input_date.strftime("%Y-%m-%d")

# import requests
# response = requests.get("https://upload.pypi.org/legacy/")
# print(response.status_code)

import certifi
print(certifi.where())
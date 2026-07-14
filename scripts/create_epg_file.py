"""Creates the .xml file.

Develop a webscraper that me to extract the
program information from the live stream website.
The program will:
1. Grab the HTML file.

2. Use beautifulsoup to narrow down the program
information.

3. Organize the program information into an xml
file using xmltree (built-in).

4. Create the xml file.
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import requests

def main():
    print(get_html("https://www.megavisiontvrd.com/#programacion"))

def get_html(link:str) -> str:
    """Gets the html file in the form of a string."""
    response = requests.get(link)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")
    raw_epg = soup.find("div", class_="schedule-container")
    #raw_epg = selected_section.get_text(strip=True)
    return raw_epg

if __name__ == "__main__":
    main()
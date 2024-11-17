import requests
from bs4 import BeautifulSoup
import re

MAX_PATH_DEPTH = 4  # Max slashes in the URL

def crawl_site():
    """
    Crawls the website 'https://tehisintellekt.ee/' and extracts text from linked pages.
    
    Returns:
        dict: A dictionary where keys are URLs and values are the processed page texts.
    """
    pages = {}
    r = requests.get('https://tehisintellekt.ee/', timeout=6)
    soup = BeautifulSoup(r.text, "html.parser")
    # Clean up redundant newlines in the page text using regex.
    pattern = r"(\n)(\n+)"
    processed_text = re.sub(pattern, r"\1", soup.text)
    pages["https://tehisintellekt.ee/"] = processed_text
    for link_tag in soup.find_all('a'):
        link = link_tag.get('href')
        # Check if the link is valid for crawling:
        # - Starts with the base URL
        # - Has a maximum of 4 slashes
        # - Is not already in the 'pages' dictionary
        # - Does not contain a fragment (i.e., '#')
        if link and link.startswith("https://tehisintellekt.ee") and link.count('/')<=MAX_PATH_DEPTH and not link in pages and not "#" in link:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, "html.parser")
            processed_text = re.sub(pattern, r"\1", soup.text)
            pages[link] = processed_text
    return pages
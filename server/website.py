import re
import requests


def scrape_website(url):
    html = requests.get(url).text
    title = re.findall(r"<title>(.*?)</title>", html)[0]

    return f"""INSERT INTO reference VALUES ("{url}", "{title}", 3);
INSERT INTO website VALUES ("{url}", UTC_TIME()); 
"""

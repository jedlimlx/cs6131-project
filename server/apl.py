import re
import datetime
import requests


def scrape_apl(doi):
    url = f"https://aip.scitation.org/doi/full/{doi}"
    html = requests.get(url).text.replace("\n", "")

    authors = re.findall(r'<a href="/author/.*?"> (.*?)</a>', html)
    title = re.findall(r'<li class="title">(.*?)</li>', html)[0]
    volume = re.findall(r'<div class="publicationContentCitation">.*?<b>(\d+)</b>', html)[0]
    number = re.findall(r'<div class="publicationContentCitation">.*?<b>\d+</b>, (\d+) \(\d+\);', html)[0]

    journal = re.findall(r'<a href=".*?" title="Journal Home">(.*?)</a>', html)[0]

    date = re.findall(r'Published Online: (.*?)</span>', html)[0].strip()
    datetime_obj = datetime.datetime.strptime(date, '%d %B %Y')
    date = datetime_obj.strftime("%Y-%m-%d")

    output = f"""
INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO journalArticle VALUES ("{doi}", "{journal}", NULL, NULL, {number}, {volume}, "{date}");
"""
    for author in authors:
        output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'

    return output

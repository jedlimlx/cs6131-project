import re
import requests


def scrape_nature(doi):
    id = doi.replace("10.1038/", "")
    html = requests.get(f"https://www.nature.com/articles/{id}").text
    title = re.findall(r'<h1 class="c-article-title" data-test="article-title" '
                       r'data-article-title="">(.*?)</h1>', html)[0]
    authors = re.findall(r'<a data-test="author-name".*?>(.*?)</a>', html)
    authors = [re.sub(r'<(.*?)>', '', x) for x in authors]

    volume = re.findall(r'<b data-test="journal-volume"><span class="u-visually-hidden">volume</span> (.*?)</b>', html)[0]
    page_start = re.findall(r'"pageStart":"(\d+)"', html)[0]
    page_end = re.findall(r'"pageEnd":"(\d+)"', html)[0]
    date = re.findall(r'"datePublished":"(\d+-\d+-\d+)"', html)[0]

    output = f"""INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO journalArticle VALUES ("{doi}", "Nature", {page_start}, {page_end}, NULL, {volume}, "{date}");
"""
    for author in authors:
        output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'

    return output

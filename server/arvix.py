import re
import requests


def scrape_arxiv(doi):
    id = doi.replace("10.48550/arXiv.", "")
    html = requests.get(f"https://arxiv.org/abs/{id}").text

    authors = re.findall(r'<div class="authors">(.*?)</div>', html)[0]
    authors = re.findall(r'<a href=".*?">(.*?)</a>', authors)
    title = re.findall(r'<h1 class="title mathjax"><span class="descriptor">Title:</span>(.*?)</h1>', html)[0]

    output = f'INSERT INTO reference VALUES ("10.48550/arXiv.{id}", "{title}", "conference");\n'
    for a in authors:
        output += f'INSERT INTO authors VALUES ("10.48550/arXiv.{id}", "{a}");\n'

    return output

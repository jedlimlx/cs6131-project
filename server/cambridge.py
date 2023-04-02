import re
import requests
import datetime


def scrape_cambridge(doi):
    html = requests.get(f"https://doi.org/{doi}").text  # .replace("\n", "").replace("  ", "")
    journal = re.findall(r'<meta name="citation_journal_title" content="(.*?)">', html)[0]
    title = re.findall(r'<meta name="citation_title" content="(.*?)">', html)[0]
    authors = re.findall(r'<meta name="citation_author" content="(.*?)">', html)
    date = datetime.datetime.strptime(
        re.findall(r'<meta name="citation_online_date" content="(.*?)">', html)[0],
        '%Y/%m/%d'
    )
    volume = re.findall(r'<meta name="citation_volume" content="(\d+)">', html)[0]

    output = f"""
INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO journalArticle VALUES ("{doi}", "{journal}", NULL, NULL, NULL, {volume}, "{date}");
"""
    for author in authors:
        output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'

    return output


if __name__ == "__main__":
    print(scrape_cambridge("10.1017/jfm.2023.151"))

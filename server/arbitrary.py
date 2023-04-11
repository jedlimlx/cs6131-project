import re
import datetime
import requests


def doi2bib(doi):
    url = "http://dx.doi.org/" + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)

    return r.text


def parse_bib(bibitem, journals):
    output = ""
    doi = re.findall(r"doi = {(.*?)}", bibitem)[0]

    day = max(list(map(int, re.findall(r"day = (\d+)", bibitem))) + [1])
    year = max(list(map(int, re.findall(r"year = (\d+)", bibitem))) + [1])
    month = max(re.findall(r"month = {(.*?)}", bibitem) + ['a'])

    authors = re.findall(r"author = {(.*?)}", bibitem)
    if len(authors) == 0:
        authors = []
    else:
        authors = authors[0].split(" and ")

    title = re.findall(r"title = {(.*?)}.\n", bibitem)[0]
    if "@article" in bibitem:
        journal = re.findall(r"journal = {(.*?)}.?\n", bibitem)[0]
        if journal not in journals:
            output += f"INSERT INTO publisher VALUES ('{journal}', NULL, 0, NULL);\n"

        volume = re.findall(r"volume = {(.*?)}", bibitem)
        if len(volume) == 0: volume = "NULL"
        else: volume = volume[0]

        number = re.findall(r"number = {(.*?)}", bibitem)
        if len(number) == 0: number = "NULL"
        else: number = number[0]

        pages = re.findall(r"pages = {(\d+)--(\d+)}", bibitem)
        if len(pages) == 0:
            pages = ["NULL", "NULL"]
        else: pages = pages[0]

        if month == "a": month = "jan"
        datetime_obj = datetime.datetime.strptime(f"{day} {month} {year}", '%d %b %Y')
        date = datetime_obj.strftime("%Y-%m-%d")

        output += f"""INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO journalArticle VALUES ("{doi}", "{journal}", {pages[0]}, {pages[1]}, {number}, {volume}, "{date}");\n"""
        for author in authors:
            output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'

        journals.append(journal)
    elif "@inproceedings" in bibitem or "@incollection" in bibitem:
        journal = re.findall(r"booktitle = {(.*?)}.?\n", bibitem, re.MULTILINE)[0]
        if journal not in journals:
            output += f"INSERT INTO publisher VALUES ({journal}, NULL, 1, NULL);\n"

        output += f"""INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO conferenceArticle VALUES ("{doi}", "{journal}", {year});\n"""
        for author in authors:
            output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'

        journals.append(journal)
    elif "@misc" in bibitem:
        journal = re.findall(r"publisher = {(.*?)}.?\n", bibitem, re.MULTILINE)[0]
        if journal not in journals:
            output += f"INSERT INTO publisher VALUES ({journal}, NULL, 0, NULL);\n"

        output += f"""INSERT INTO reference VALUES ("{doi}", "{title}", 0);
INSERT INTO journalarticle VALUES ("{doi}", "{journal}", NULL, NULL, NULL, NULL, NULL);"""
        for author in authors:
            output += f'INSERT INTO authors VALUES ("{doi}", "{author}");\n'
            
    return output


def scrape_arbitrary(doi, journals):
    return parse_bib(doi2bib(doi), journals)

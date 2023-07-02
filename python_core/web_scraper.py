import re
from pathlib import Path
import string
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.nature.com"


def input_pages():
    return int(input())


def input_type():
    return input()


def fetch_content(url):
    response = requests.get(url, timeout=5)
    if response:
        return response.content, response.status_code
    return b"", response.status_code


def find_type(soup):
    tag = soup.select_one(".c-meta__type")
    return tag.text if tag else ""


def find_link(soup):
    tag = soup.select_one('a[href^="/articles/"]')
    text = tag.text if tag else ""
    url = BASE_URL + tag.attrs["href"]
    return url, text


def make_safe_text(text):
    pattern = f"[{string.punctuation}]"
    temp = re.sub(pattern, " ", text)
    return re.sub(" +", "_", temp.strip())


def main():
    url = f"{BASE_URL}/nature/articles?sort=PubDate&year=2020"

    pages = input_pages()
    type_ = input_type()

    for i in range(1, pages + 1):
        directory = Path(f"Page_{i}")
        directory.mkdir(parents=True, exist_ok=True)
        page_url = f"{url}&page={i}"
        content, status_code = fetch_content(page_url)
        if status_code >= 400:
            continue

        soup = BeautifulSoup(content, "html.parser")
        rows = soup.select("#new-article-list ul.app-article-list-row > li")
        for row in rows:
            article_url, article_title = find_link(row)
            article_type = find_type(row)
            if type_ != article_type:
                continue

            safe_title = make_safe_text(article_title)
            filepath = directory / (safe_title + ".txt")

            article_content, _ = fetch_content(article_url)
            article_soup = BeautifulSoup(article_content, "html.parser")
            article_body = article_soup.select_one("p.article__teaser")
            if not article_body:
                continue
            with filepath.open("wb") as f:
                f.write(article_body.get_text().encode().strip())

    print("Saved all articles.")


if __name__ == "__main__":
    main()

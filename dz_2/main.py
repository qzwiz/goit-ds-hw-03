from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests
from bs4 import BeautifulSoup
import json

client = MongoClient(
    "mongodb+srv://darkwiz:pososed222999@cluster0.0h6op.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi("1"),
)

db_2 = client.dz_2
qoutes = client.dz_2.qoutes
authors = client.dz_2.authors

url = "https://quotes.toscrape.com/"


def get_author_about(url_1):
    response = requests.get(url_1)
    soup = BeautifulSoup(response.text, "lxml")
    fullname = soup.find("h3", class_="author-title").text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }


def all_qoutes(url):
    result_qoutes = []
    result_authors = []
    seen_authors = set()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        all_qoutes = soup.find_all("div", class_="quote")

        for qoute in all_qoutes:
            author = qoute.find("small", class_="author").text.strip()
            text = qoute.find("span", class_="text").text.strip()
            tags = [tag.text for tag in qoute.find_all("a", class_="tag")]

            result_qoutes.append({"author": author, "quote": text, "tags": tags})

            if author not in seen_authors:
                find_author = qoute.find("a").get("href")
                author_url = "https://quotes.toscrape.com" + find_author
                author_about = get_author_about(author_url)
                result_authors.append(author_about)
                seen_authors.add(author)

        next_btn = soup.find("li", class_="next")
        if next_btn:
            url = "https://quotes.toscrape.com" + next_btn.find("a")["href"]
        else:
            url = None

    return result_qoutes, result_authors


def main():
    url = "https://quotes.toscrape.com/"
    quotes, authors = all_qoutes(url)

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, indent=4, ensure_ascii=False)


    db_2.qoutes.insert_many(quotes)  
    db_2.authors.insert_many(authors)

    print("ну все")


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {"User-Agent": user}

HOST = "https://hauntedmound.com"
LINK = "https://shop.hauntedmound.com"
FILE = "merch.csv"

def get_content(link):
    r = requests.get(link, headers=headers)
    return r

def get_items(link):
    soup = BeautifulSoup(get_content(link).text, "html.parser")
    items = soup.find_all("li", class_="grid__item")
    merch = []
    for item in items:
        merch.append(
            {
                "title": item.find("h3", class_="card-information__text").get_text().strip(),
                "price": item.find("span", class_="price-item").get_text().strip(),
                "link": LINK + item.find("a").get("href"),
            })
    return merch

def save_content(merch):
    with open(FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Title", "Price", "Link"])
        for i in merch:
            writer.writerow([i["title"], i["price"], i["link"]])

def parser():
    html = get_content(LINK)
    if html.status_code == 200:
        save_content(get_items(LINK))
        print("Successful!")
    else:
        print("Something went wrong! Damn......")

parser()
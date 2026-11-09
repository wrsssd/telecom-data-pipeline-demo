import csv
import requests
from bs4 import BeautifulSoup


BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def parse_books(pages=3):
    results = []

    for page in range(1, pages + 1):
        resp = requests.get(BASE_URL.format(page), headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            print(f"Page {page} skipped (status {resp.status_code})")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")

        for item in items:
            title = item.h3.a["title"]
            raw_price = item.find("p", class_="price_color").text
            price = float(raw_price.replace("£", "").replace("Â", ""))
            stock = item.find("p", class_="instock availability").text.strip()

            results.append({
                "title": title,
                "price_gbp": price,
                "availability": stock,
                "page": page
            })

    return results


def save_to_csv(data, filename="books_dataset.csv"):
    if not data:
        return

    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data)} items to {filename}")


if __name__ == "__main__":
    books = parse_books(pages=3)
    save_to_csv(books)

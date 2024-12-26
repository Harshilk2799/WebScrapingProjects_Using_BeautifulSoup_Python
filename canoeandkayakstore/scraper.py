from bs4 import BeautifulSoup
import grequests
import pandas as pd

# grequest library
# = grequests is a Python library that enables asynchronous HTTP requests using gevent for concurrent operations.
# Core Features:
# 1. Makes multiple HTTP requests concurrently
# 2. Uses gevent for asynchronous I/O
# 3. Significantly faster than sequential requests

def get_urls():
    urls = []
    for i in range(1,5):
        urls.append(f"https://www.canoeandkayakstore.co.uk/collections/clothing-1?page={i}")
    return urls 

def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp 


def get_parse(resp):
    productlists = []
    for r in resp:
        soup = BeautifulSoup(r.text, "lxml")
        records = soup.select("div#filter-results ul li.js-pagination-result")
        print("Length: ", len(records))
        for record in records:
            try:
                product_name = record.select_one("p.card__title a").text
            except:
                product_name = None
            print("Item Name: ", product_name)

            try:
                current_price = record.select_one("div.price__default strong.price__current").text
            except:
                current_price = None
            print("Current Price: ", current_price)

            try:
                product_link = "https://www.canoeandkayakstore.co.uk" + record.select_one("p.card__title a")["href"]
            except:
                product_link = None 
            print("Item Link: ", product_link)

            product_detail = {
                    "Product Name": product_name.strip(),
                    "Current Price": current_price.strip(),
                    "Product Link": product_link.strip()
                }

            productlists.append(product_detail)

    return productlists

if __name__ == "__main__":
    urls = get_urls()
    resp = get_data(urls)
    result = get_parse(resp)
    df = pd.DataFrame(result)
    df.to_csv("Product.csv", index=False)
from bs4 import BeautifulSoup
import requests
import pandas as pd

try:
    books = []
    for i in range(1, 3):
        pagination_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
        # print(pagination_url)
        res = requests.get(pagination_url)

        soup = BeautifulSoup(res.content, "lxml")

        books_link = soup.select("ol.row li h3")

        for book_link in books_link:
            bookLink = "https://books.toscrape.com/catalogue/" + book_link.select_one("a")["href"]
            # print(bookLink)
            book_response = requests.get(bookLink, headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"})
            # print("Status: ", book_response.status_code)
            if book_response.status_code == 200:
                book_soup = BeautifulSoup(book_response.content, "lxml")

                # Book Title
                try:
                    book_title = book_soup.select_one("h1").text
                except: 
                    book_title = None
                print("Book Title: ", book_title)

                # Book Price
                try:
                    book_price = book_soup.select_one("p.price_color").text
                except:
                    book_price = None
                print("Book Price: ", book_price)
                
                # Book Img
                try:
                    book_img = book_soup.select_one("div.item.active img")["src"]
                    new_book_img = "https://books.toscrape.com/" + book_img.split("../../")[-1]
                except:
                    new_book_img = None
                print("Book Image: ", new_book_img)

                # Book Description
                try:
                    book_description = book_soup.select_one("div#product_description + p").text
                except:
                    book_description = None
                print("Book Description: ", book_description)

                print("==========================")

                books.append({
                    "Book URL": bookLink,
                    "Book Title": book_title,
                    "book_price": book_price,
                    "Book Image": new_book_img,
                    "Book Description": book_description
                })

            # break

        print(f"==========================={i}=================================")

    df = pd.DataFrame(books)
    df.to_csv("Books.csv", index=False)

except Exception as e:
    print(e)

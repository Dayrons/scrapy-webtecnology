import requests
from bs4 import BeautifulSoup
import pandas as pd

def send_email():
   pass

def generate_excel(products):

    df = pd.DataFrame(products)
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
 

def scrapy() -> list:
    url = 'https://compupalace.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page= requests.get(url=url, headers=headers)
    page_parse = BeautifulSoup(page.content, "html.parser")


    results = page_parse.find_all("div", class_="product-grid-item")

    products = []
    for product in results:

        try:
            title =product.find("h3", class_="wd-entities-title").get_text()
            categories = product.find("div", class_="wd-product-cats").get_text()
            price = product.find("span", class_="price").get_text()
            products.append({"title":title, "categories":categories, "price": price})
        except:
            print("Hubo un error")
    
    return products


 


if "__main__" == __name__:
    
    generate_excel(scrapy())

    send_email()
    
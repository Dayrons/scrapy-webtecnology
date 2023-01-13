import requests
from bs4 import BeautifulSoup
import pandas as pd
from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()


def send_email():

    try:
   
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Reporte de precios Compupalace'
        mensaje['From']=os.getenv('EMAIL_FROM')
        mensaje['To']=os.getenv("EMAIL_TO")
        html = f"""
        <html>
            <body>
                <h1>Reporte de precios de sitio web <a href="https://compupalace.com/">Compupalace</a> </h1>
            </body>

        </html>

        """
        parte_html = MIMEText(html,'html')
        mensaje.attach(parte_html)

       
        file = MIMEBase('application', 'octet-stream')
        file.set_payload(open('report.xlsx', 'rb').read())
        encoders.encode_base64(file)
        file.add_header('content-Disposition','attachment; filename="report.xlsx"')
        mensaje.attach(file)


        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        server.login(mensaje['From'],os.getenv('EMAIL_PASSWORD_FROM'))
        server.sendmail(from_addr=mensaje['From'], to_addrs=mensaje['To'], msg=mensaje.as_string() )
        server.quit()

    except :
        print("Error al enviar correo")



        

def generate_excel(products):

    df = pd.DataFrame(products)
    writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')
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
            print("Hubo un error al obtener informacion")
    
    return products


 


if "__main__" == __name__:
    
    # generate_excel(scrapy())

    send_email("dayronstovar@gmail.com")
    
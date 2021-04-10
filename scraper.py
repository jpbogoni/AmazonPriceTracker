import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

chromedriver_loc = '/home/jpbogoni/Python/chromedriver'
driver = webdriver.Chrome(chromedriver_loc, chrome_options=chrome_options)

email_login = input("e-mail login")
email_password = input("e-mail password")
email_to = input("e-mail to")

class Product:
    def __init__(self, url, price_target):
        self.url = url
        self.price_target = price_target

def product_list():
    products = []
    products.append( Product('https://www.amazon.com.br/gp/product/B07T39FC9P/ref=ewc_pr_img_2?smid=A1ZZFT5FULY4LN&psc=1',1800))
    products.append( Product('https://www.amazon.com.br/Microsoft-Console-Xbox-Series-S/dp/B08JN2VMGX/ref=sr_1_1?dchild=1&keywords=xbox+series+x&qid=1618078279&sr=8-1',2900))
    products.append( Product('https://www.amazon.com.br/Apple-MacBook-Pro-Chip-256GB/dp/B08N5N6RSS/ref=sr_1_1_sspa?dchild=1&keywords=m1&qid=1618078330&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyVFhGT0daQ0ZCRUtaJmVuY3J5cHRlZElkPUEwNjI3MjM0MUc5N00wQzdMUDg2NyZlbmNyeXB0ZWRBZElkPUEwODk2NjI4MVhKM1JROEkzMzNBMSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=',11000))
    return products

def price_check(Product):
    #Implemntar parametros URL; Price
    URL = Product.url #'https://www.amazon.com.br/gp/product/B07T39FC9P/ref=ewc_pr_img_2?smid=A1ZZFT5FULY4LN&psc=1'

    get = driver.get(URL)

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice")
    if price is None:
        price = soup.find_all("span", class_="a-size-medium a-color-price priceBlockSavingsString")
        #priceText = soup.find_all("span", class_="a-size-medium a-color-price priceBlockSavingsString")
    else:
        price = price.get_text()

    converted_price = float(price[2:len(price)-3])
    
    if (converted_price < Product.price_target):
        send_email(title, price, URL)

def send_email(product, price, url):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email_login,email_password)

    subject = "Price check for " + product
    body = product + ' is available for ' + price + '  URL: ' + url

    msg = (f"Subject: {subject}  {body}").encode('utf-8')
    #print (msg)
    server.sendmail(email_login,email_to,msg)

    #print (msg)


check = product_list()

for item in check:
    price_check(item)

print ('END CHECK!')

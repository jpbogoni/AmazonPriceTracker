import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

chromedriver_loc = '/home/jpbogoni/Python/chromedriver'
driver = webdriver.Chrome(chromedriver_loc, chrome_options=chrome_options)

def price_check():
    URL = 'https://www.amazon.com.br/gp/product/B07T39FC9P/ref=ewc_pr_img_2?smid=A1ZZFT5FULY4LN&psc=1'

    get = driver.get(URL)

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()

    converted_price = float(price[2:len(price)])

    if (converted_price < 1200):
        send_email()

    #print(title.strip())
    #print(converted_price)

def send_email():
    
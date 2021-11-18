from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

ser = Service(PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(service=ser, options=options)
url = "https://novelfull.com/super-gene/chapter-2731-god-body-evolved.html"
browser.get(url)
time.sleep(10)
html = browser.page_source
soup = BeautifulSoup(html , 'html.parser')
with open('scraped.txt', 'w') as file:
    file.write(str(soup))

browser.quit()


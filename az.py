from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

ser = Service(PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=ser, options=options)

url = "https://www.itexams.com/exam/AZ-104?"

driver.get(url)
print(driver.title)

question_containers = driver.find_elements(By.CLASS_NAME,'card')
for question_container in question_containers:
    
    showAnswer = WebDriverWait(question_container, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "show_answer"))
    )    
    showAnswer.click()


time.sleep(5)    
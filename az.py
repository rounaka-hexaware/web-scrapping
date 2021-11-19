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
login = driver.find_element(By.LINK_TEXT,"Login")
login.click()
username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
    )
username.send_keys("rounakagrawal")
password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_password"))
    )
password.send_keys("Password@1234")
password.send_keys(Keys.RETURN)
driver.get(url)
questions = []



question_containers = driver.find_elements(By.CLASS_NAME,'card')
for question_container in question_containers:
    
    showAnswer = WebDriverWait(question_container, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "show_answer"))
    )    
    showAnswer.click()
    questionBlock = WebDriverWait(question_container, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "question_block"))
    )    
    questions.append(questionBlock.get_attribute('innerHTML'))
soup = BeautifulSoup(questions, 'html.parser')
with open('questions.txt', 'w') as file:
    file.write(str(soup.encode("utf-8")))

time.sleep(5) 
driver.quit()   
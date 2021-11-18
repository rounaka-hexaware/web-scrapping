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

url = "https://www.examtopics.com/exams/microsoft/az-204/view/"

driver.get(url)
print(driver.title)

question_cards = driver.find_elements(By.CLASS_NAME,'exam-question-card')
for question_card in question_cards:
    
    revealSolution = WebDriverWait(question_card, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "reveal-solution"))
    )    
    revealSolution.click()
questions = driver.find_elements(By.CLASS_NAME,'question-body')
for question in questions:
    
    cardText = WebDriverWait(question, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-text"))
    )
    questionChoices = WebDriverWait(question, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "question-choices-container"))
    )
    print(cardText.get_attribute('innerHTML'))
       
    
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html , 'html.parser')
with open('examTopics.txt', 'w') as file:
    file.write(str(soup.encode("utf-8")))

time.sleep(5)
driver.quit()
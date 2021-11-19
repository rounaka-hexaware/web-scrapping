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
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=ser, options=options)

url = "https://www.itexams.com/exam/AZ-104?"

driver.get(url)
print(driver.title)
login = driver.find_element(By.LINK_TEXT, "Login")
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


question_containers = driver.find_elements(By.CLASS_NAME, 'card')
for question_container in question_containers:

    showAnswer = WebDriverWait(question_container, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "show_answer"))
    )
    showAnswer.click()
    questionBlock = WebDriverWait(question_container, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "question_block"))
    )
    questions.append(questionBlock.get_attribute('innerHTML'))

nextButton = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "open-captcha"))
)
nextButton.click()
time.sleep(5)
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

# html = driver.page_source
# soup = BeautifulSoup(html , 'html.parser')
# with open('exam.html', 'w') as file:
#     file.write(str(soup.prettify().encode("utf-8")))
# file = open("questions.html","w")
# for question in questions:
#     soup = BeautifulSoup(question, 'html.parser')
#     file.write(str(soup.prettify().encode("utf-8")))
#     print(soup.get_text())


time.sleep(5)
# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get("https://novelfull.com/")

print(driver.title)

search = driver.find_element_by_id("search-input")

search.send_keys("super gene")
search.send_keys(Keys.RETURN)
chap_name = []

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Super Gene"))
    )
    element.click()  
    chapter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Chapter 1: Supergene"))
    )
    chapter.click()
    for i in range(5):
        chapter_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chapter-text"))
        )
        chap_name.append(chapter_name.text)
        next_button = driver.find_element_by_id("next_chap")
        next_button.click()
    print(chap_name)
    

except:
    time.sleep(5)
    driver.quit()


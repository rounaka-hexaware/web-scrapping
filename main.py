# Import package dependencies
import os
import sys
from bs4 import BeautifulSoup
import requests
import lxml
import numpy as np
import csv
import json
import numpy
import copy
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service



# Configure the path to the directory containing the data files
domain = 'https://www.itexams.com'
exam_code = '/exam/AZ-900?'
url = domain + exam_code

PATH = "C:\Program Files (x86)\chromedriver.exe"

ser = Service(PATH)
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=ser, options=options)

driver.get(url)
print(driver.title)
time.sleep(2)
login = driver.find_element(By.LINK_TEXT,"Login")
login.click()
time.sleep(2)
username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
    )
username.send_keys("rounakagrawal")
password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_password"))
    )
password.send_keys("Password@1234")
password.send_keys(Keys.RETURN)
time.sleep(2)
driver.get(url)

def parse_url_from_text(text):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)      
    return [x[0] for x in url]


def remove_url_from_text(text):
    text = re.sub(r'http\S+', '', text)
    text = text.replace('Reference:', '')
    return text


def blank_character_cleaner(text):
    text = text.replace('\n', '').replace('\t', '').lstrip()
    return text


def fetch_data(url):
    response = requests.get(url)
    return response.text


def parse_data(data):
    soup = BeautifulSoup(data, 'lxml')
    each_question_card = soup.findChildren('div', {'id': 'accordion'}, recursive=True)[0]
    each_question_card_element = each_question_card.findChildren('div', {'class': 'card'}, recursive=True)
    return each_question_card_element


data = parse_data(fetch_data(url))
print("Number of questions : {}".format(len(data)))



data_output = list()
time.sleep(2)
for i in range(1):
    for i in range(len(data)):

        data_payload = data[i].findChildren(recursive=True)

        question_id = blank_character_cleaner(data_payload[0].findChildren(recursive=True)[0].text.replace(' ', ''))
        question_payload = blank_character_cleaner(data_payload[4].findChildren(recursive=True)[0].find_all('p')[2].text)
        question_statement = blank_character_cleaner(data_payload[4].findChildren(recursive=True)[0].find_all('p')[0].text)
        question_answer_key = blank_character_cleaner(data_payload[4].findChildren(recursive=True)[0].find_all('p')[1].text)
        # question_answer_image = data_payload[4].findChildren(recursive=True)[0].find_all('img')[1]['src']
        question_answer_key = question_answer_key.replace('Answer :', '').lstrip()
        image_payload = data_payload[4].findChildren(recursive=True)[0].find_all('img')

        question_image = ''
        answer_image = ''
        if len(image_payload) != 0:
            if (len(image_payload) == 1):
                question_image = domain + image_payload[0]['src']
            if (len(image_payload) == 2):
                question_image = domain + image_payload[0]['src']
                answer_image = domain + image_payload[1]['src']

        reference_links = parse_url_from_text(question_payload)

        question_explaination = remove_url_from_text(question_payload)

        reference_link_1 = ''
        reference_link_2 = ''
        if (len(reference_links) != 0):
            if (len(reference_links) == 1):
                reference_link_1 = reference_links[0]
            if (len(reference_links) == 2):
                reference_link_1 = reference_links[0]
                reference_link_2 = reference_links[1]
        
        data_parsed = {
            "question_id": question_id,
            "question_statement": question_statement,
            "question_answer_key": question_answer_key,
            "question_image": question_image,
            "answer_image": answer_image,
            "question_explaination": question_explaination,
            "reference_link_1": reference_link_1,
            "reference_link_2": reference_link_2
        }

        
        data_output.append(data_parsed)
        # print("QuestionId : {}\n".format(question_id))
        # print('Question_Statement : {}\n'.format(question_statement))
        # print('Question_Image : {}\n'.format(question_image))
        # print('Question_Answer_key : {}\n'.format(question_answer_key))
        # print('Question_Answer_image : {}\n'.format(answer_image))
        # print('Question_Explaination : {}\n'.format(question_explaination))
        # print('Reference Links : \n', reference_links)
    time.sleep(5)
    nextButton = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//button[@title='Next Page']"))
    )
    nextButton.click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()



# print(data_output)
# data_list = json.dumps(data_output)
# print(type(data_output))

df = pd.json_normalize(data_output)
df.head(len(data_output))
df.to_csv('data.csv', index=False)






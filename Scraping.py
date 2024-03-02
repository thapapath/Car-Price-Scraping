import re
import csv
import pandas as pd
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

chrome_options = Options()

website = 'https://www.roddonjai.com/?activeMenu=3'
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)
driver.get(website)
time.sleep(3)

try:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/button"))).click()
except Exception as e:
    print(e)
    
try:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cmp-btn-granted"]'))).click()
except Exception as e:
    print(e)


# Importing necessary libraries
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

# Set up Chrome webdriver options and the target website
chrome_options = Options()
website = 'https://www.roddonjai.com/?activeMenu=3' 
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = webdriver_service, options = chrome_options)
driver.get(website)
time.sleep(3)  # Add delay to ensure page is fully loaded

# Close pop-up ads button
try:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/button"))).click()
except Exception as e:
    print(e)

# Close first-party cookies panel
try:
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cmp-btn-granted"]'))).click()
except Exception as e:
    print(e)

# Create a list of provinces in Thailand to filter the TAG_NAME 'p' since XPATH is not working
province_TH = [
    "กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", 
    "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", 
    "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", 
    "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", 
    "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", 
    "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", 
    "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", 
    "สมุทรสงคราม", "สมุทรสาคร", "สระแก้ว", "หนองบัวลำภู", "สระบุรี", "สิงห์บุรี", "สุโขทัย", 
    "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "หนองคาย", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", 
    "อุตรดิตถ์", "อุทัยธานี", "อุบลราชธานี"
]

# Find the total number of pages to use for loops
button_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/main/div/div/div/div[2]/div/section/div/div/div/div[2]/div[1]/nav/ul/li[5]/button')
page_number_text = button_element.text
page_number = int(page_number_text)

# Create empty lists to store items
car_names = []
model_names = []
province_names = []
prices = []
mileages = []

# Loop through each page to scrape data
for page_num in range(page_number - 2):
    wait = WebDriverWait(driver, 10)

    # Find the current page number to track progress
    current_page_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/main/div/div/div/div[2]/div/section/div/div/div/div[2]/div[1]/nav/ul/li[3]/button')
    current_page_text = current_page_element.text
    current_page = int(current_page_text)

    # Find the name of the car from h2 elements
    car_elements = driver.find_elements(By.TAG_NAME, 'h2')
    for car in car_elements:
        car_names.append(car.text)
        
    # Find the model name of the car from h3 elements
    model_elements = driver.find_elements(By.TAG_NAME, 'h3')
    for model in model_elements:
        model_names.append(model.text)

    # Find the province of the car from p elements by filtering with province_TH list
    province_elements = driver.find_elements(By.TAG_NAME, 'p')
    for province in province_elements:
        try:
            if province.text.strip() in province_TH:
                province_names.append(province.text)
        except StaleElementReferenceException:
            # Re-locate the elements if they become stale
            province_elements = driver.find_elements(By.TAG_NAME, 'p')
            continue

    # Find the price of the car from p elements using REGEX to filter only those ending with .- and remove commas
    price_elements = driver.find_elements(By.TAG_NAME, 'p')
    pattern_thb = r'^(.*)\.-$'
    for price in price_elements:
        try:
            match = re.match(pattern_thb, price.text)
            if match:
                price_value = int(match.group(1).replace(',', ''))
                prices.append(price_value)
        except StaleElementReferenceException:
            # Re-locate the elements if they become stale
            price_elements = driver.find_elements(By.TAG_NAME, 'p')
            continue
            
    # Find the mileage of the car from p elements using REGEX to filter only those ending with กม. and remove commas
    mileage_elements = driver.find_elements(By.TAG_NAME, 'p')
    pattern_km = r'^([\d,]+)\sกม\.$'
    for mileage in mileage_elements:
        try:
            match = re.match(pattern_km, mileage.text)
            if match:
                mileage_value = int(match.group(1).replace(',', ''))
                mileages.append(mileage_value)
        except StaleElementReferenceException:
            # Re-locate the elements if they become stale
            mileage_elements = driver.find_elements(By.TAG_NAME, 'p')
            continue

    # Find the next page button and click
    try:
        wait = WebDriverWait(driver, 20)
        next_button_xpath = "//button[contains(., 'ถัดไป')]"
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()

    except ElementClickInterceptedException:
        # If ElementClickInterceptedException occurs, wait for a moment and retry clicking
        time.sleep(1)  # Adjust the delay time as needed
        next_button.click()

    except Exception as e:
        print(f"An error occurred on page {current_page + 1}: {e}")
        continue

    # Save data to CSV after scraping each page
    cars_info = {
        'Name': car_names,
        'Model': model_names,
        'Province': province_names,
        'Price': prices,
        'Mileage': mileages
    }

    # Convert dictionary to DataFrame and save as CSV
    df = pd.DataFrame(cars_info)
    df.to_csv('cars_info.csv', index=False)
    
    print(f"Page: {current_page}: Total list in car_names = {len(car_names)}")
    
print(f"Scraping up to page {current_page}/{page_number}. Data saved to 'cars_info.csv'.")

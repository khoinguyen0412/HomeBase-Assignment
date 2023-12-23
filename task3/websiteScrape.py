from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
import undetected_chromedriver
import json
import os
import sys


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--start-maximized')
options.add_argument('--disable-popup-blocking')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Add the necessary Permissions-Policy header

chromedriver_autoinstaller.install()
driver = undetected_chromedriver.Chrome(options=options)
delay = 5


driver.get("https://batdongsan.com.vn/nha-dat-ban")

def wait_page():
    try:
        myElem = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-product-id]')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")
        driver.close()
        sys.exit()



def get_info_by_page():
    section = driver.find_elements(By.CSS_SELECTOR, '[data-product-id]') 
    new_list = []
    for item in section:
        title = item.get_attribute('title')
        price = item.find_element(By.CLASS_NAME,'re__card-config-price').text
        location = item.find_element(By.CLASS_NAME,'re__card-config-area').text
        description = item.find_element(By.CLASS_NAME,'re__card-description').text

        new_obj = {
            title: title,
            price: price,
            location: location,
            description:description
        }

        new_list.append(new_obj)

    with open(file_path, 'r',encoding='utf-8') as json_file:
        existing_data = json.load(json_file)

    existing_data.extend(new_list)

    with open(file_path, 'w',encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=2,ensure_ascii=False)


file_path = './task3/output.json'

if not os.path.exists(file_path):
    existing_data = []
    with open(file_path, 'w',encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=2)

    section = driver.find_elements(By.CSS_SELECTOR, '[data-product-id]') 

    new_list = []
    for item in section:
        title = item.get_attribute('title')
        price = item.find_element(By.CLASS_NAME,'re__card-config-price').text
        location = item.find_element(By.CLASS_NAME,'re__card-config-area').text
        description = item.find_element(By.CLASS_NAME,'re__card-description').text

        new_obj = {
            title: title,
            price: price,
            location: location,
            description:description
        }

        new_list.append(new_obj)

    with open(file_path, 'r',encoding='utf-8') as json_file:
        existing_data = json.load(json_file)

    existing_data.extend(new_list)

    with open(file_path, 'w',encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=2,ensure_ascii=False)

def main():
    wait_page()
    get_info_by_page()
    page_numbers = driver.find_elements(By.CSS_SELECTOR, '[pid]')
    max_page = 0

    for item in page_numbers:
        number = int(item.get_attribute('pid'))
        if number > max_page:
            max_page = number

    for i in range(2,max_page+1):
        page_numbers = driver.find_elements(By.CSS_SELECTOR, '[pid]')
        for item in page_numbers:
            if int(item.get_attribute('pid')) == i:
                item.click()
                break

        wait_page()
        get_info_by_page()

    driver.quit()
               
if __name__ == '__main__':
    main()

# Instead of caching mechanism, I keep track of the page I am clicking on
# I click on the page to navigate to a new page to reduce the chance of 
# of being dectected by CloudFare (Instead of using new get request)
# To prevent excessive requests, we can add a time.sleep() to handle that
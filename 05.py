from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
# options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True) # stop webdriver turning off
options.add_argument("--start-maximized") # max browser screen size
options.add_argument("--incognito")  # Using incognito mode creates a temporary profile

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

driver.get("https://www.diningcode.com/")

# 다른지역선택 버튼
selectLocationBtn = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/button[1]')
selectLocationBtn.click()

# 서울 지역 클릭
seoulBtn = driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div/div/div[2]/div[2]/ul[1]/li[1]/button')
seoulBtn.click()

# 전체 버튼 클릭
allBtn = driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div/div/div[2]/div[2]/ul[2]/li[1]/button')
allBtn.click()

# 선택 완료 버튼 클릭
submitBtn = driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div/div/div[3]/button[2]')
submitBtn.click()

# (서울 전체지역 안에 있는 406개의) 음식점들
restaurants = driver.find_elements(By.CLASS_NAME, "Slide__Card__Item")
restarurantATag = restaurants[0].find_elements(By.CSS_SELECTOR, "a")[0]
# print("restaurantATag:", restarurantATag)
restarurantATag.click()

# Switch to the newly opened tab
driver.switch_to.window(driver.window_handles[-1])

name = driver.find_element(By.XPATH, '//*[@id="div_profile"]/div[1]/div[2]/h1').text
location = driver.find_element(By.CLASS_NAME, "locat").text.split("\n")[0].split(" ")
metropolitan = location[0]
city = location[1]
district = location[2]
detailedAddress = location[3]
rating = driver.find_element(By.ID, 'lbl_review_point').text
print("name:", name)
print("metropolitan:", metropolitan)
print("city:", city)
print("district:", district)
print("detailedAddress:", detailedAddress)
print("rating:", rating)
data.append([name, metropolitan, city, district, detailedAddress, rating])


df = pd.DataFrame(data, columns=["name", "metropolitan", "city", "district", "detailedAddress", "rating"])

# index=False otherwise first column will be named index
# df.to_csv("diningcode.csv", index=False)

# Convert DataFrame to JSON
# json_data = df.to_json(orient="records")

# # Save JSON data to a file
# with open("data.json", "w", encoding='utf-8') as json_file:
#     json_file.write(json_data)

with open('data.json', 'w', encoding='utf-8') as file:
    df.to_json(file, force_ascii=False)
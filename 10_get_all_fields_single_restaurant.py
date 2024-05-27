from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


options = Options()
options.add_extension("./extensions/ad_block.crx")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []
my_restaurant = {}

driver.get("https://www.diningcode.com/")

rand = random.uniform(1, 5)

time.sleep(rand)  # wait for 5 seconds
driver.implicitly_wait(rand)  # wait until the web page shows up
main = driver.window_handles  # opened tabs
for i in main:
    if i != main[0]:
        driver.switch_to.window(i)
        driver.close()
time.sleep(rand)
driver.implicitly_wait(rand)
driver.switch_to.window(driver.window_handles[0])

# Wait until the element is clickable
wait = WebDriverWait(driver, 10)

# 다른지역선택 버튼
selectLocationBtn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[2]/div[2]/div/div[2]/button[1]')
    )
)
selectLocationBtn.click()

# 서울 지역 클릭
seoulBtn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[4]/div/div/div[2]/div[2]/ul[1]/li[1]/button')
    )
)
seoulBtn.click()

# 전체 버튼 클릭
allBtn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[4]/div/div/div[2]/div[2]/ul[2]/li[1]/button')
    )
)
allBtn.click()

# 선택 완료 버튼 클릭
submitBtn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div[4]/div/div/div[3]/button[2]')
    )
)
submitBtn.click()

action = driver.find_element(By.CSS_SELECTOR, "body")

try:
    read_more_elements = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Read__More__Text"))
    )
    read_more = read_more_elements[0]
    read_more.click()
except StaleElementReferenceException:
    # Handle stale element reference exception by locating the element again
    read_more_elements = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Read__More__Text"))
    )
    read_more = read_more_elements[0]
    read_more.click()


driver.switch_to.window(driver.window_handles[-1])

restaurants = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "InfoHeader"))
)

restaurant = restaurants[0]
restaurant.click()

# Switch to the newly opened tab
driver.switch_to.window(driver.window_handles[-1])

name = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_profile .tit"))
).text
location = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "locat")))
locationArr = location.text.split("\n")[0].split(" ")
metropolitan = locationArr[0]
city = locationArr[1]
district = locationArr[2]
detailedAddress = locationArr[3]
rating = wait.until(EC.element_to_be_clickable((By.ID, "lbl_review_point"))).text
menuList = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.list.Restaurant_MenuList")
    )
)[0]
menuList_li_tags = menuList.find_elements(By.TAG_NAME, "li")
menuAndPrice = []

print("name:", name)
print("rating:", rating)
my_restaurant["name"] = name
my_restaurant["address"] = {
    "metropolitan": metropolitan,
    "city": city,
    "district": district,
    "detailedAddress": detailedAddress,
}
my_restaurant["rating"] = rating
my_restaurant["menuAndPrice"] = []

for li in menuList_li_tags:
    menu_name = li.find_element(By.CSS_SELECTOR, "span.Restaurant_Menu").text
    price_element = li.find_element(By.CLASS_NAME, "Restaurant_MenuPrice")
    driver.execute_script("arguments[0].scrollIntoView(true);", price_element)

    # Wait for the price element to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of(price_element))

    price = price_element.text
    print("menu:", menu_name, "price:", price)
    menu_item = {"menu": menu_name, "price": price}
    my_restaurant["menuAndPrice"].append(menu_item)

my_restaurant["image"] = []

images = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-list.pic-grade"))
)[0]
img_tags = images.find_elements(By.TAG_NAME, "img")
for img_element in img_tags:
    src_value = img_element.get_attribute("src")
    my_restaurant["image"].append(src_value)

my_restaurant["location"] = {"type": "Point", "coordinates": []}
my_restaurant["category"] = [{"foodType": ""}, {"mateType": []}]
data.append(my_restaurant)


main = driver.window_handles
for i in main:
    driver.switch_to.window(i)
    driver.close()

df = pd.DataFrame(data)

with open("single_restaurant.json", "w", encoding="utf-8") as file:
    df.to_json(file, force_ascii=False)

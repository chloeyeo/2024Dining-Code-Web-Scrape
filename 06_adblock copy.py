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

options = Options()
options.add_extension("./extensions/ad_block.crx")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

driver.get("https://www.diningcode.com/")

rand = random.uniform(1, 5)

time.sleep(rand)  # wait for 5 seconds
driver.implicitly_wait(rand)  # wait until the web page shows up
main = driver.window_handles
# print("main:", main) # opened tabs
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

for i in range(25):
    # delete 키 오른쪽 바로 옆에 있는 end키를 여러번 눌러서 페이지 끝까지 내린다.
    action.send_keys(
        Keys.END
    )  # 모든 데이타가 다 불러져 온 상태에서 크롤링을 하려고 끝까지 페이지를 내린거다.


time.sleep(rand)
driver.implicitly_wait(rand)

# 서울 전체지역 안에 있는 음식점들
restaurants = driver.find_elements(By.CLASS_NAME, "Slide__Card__Item")
# while True:
#     # Scroll to the bottom of the page
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # Adjust this delay as needed

#     # Retrieve all elements with class name 'Slide__Card__Item' currently in the DOM
#     restaurants = driver.find_elements(By.CLASS_NAME, "Slide__Card__Item")

#     # Check if all restaurants are loaded
#     if len(restaurants) >= 3000:
#         break

# restaurants = wait.until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, "Slide__Card__Item"))
# )

# print("Type of restaurants:", type(restaurants))
print("Number of restaurants found:", len(restaurants))
# print("restaurants:", restaurants)

restaurants = set(restaurants)
print("Number of distinct restaurants found:", len(restaurants))

for restaurant in restaurants:
    time.sleep(rand)
    driver.implicitly_wait(rand)

    class_names = restaurant.get_attribute("class").split()
    css_selector = "." + ".".join(class_names) + " a"
    restaurantATag = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )

    time.sleep(rand)
    driver.implicitly_wait(rand)

    # Scroll to the element to ensure it's in view
    driver.execute_script("arguments[0].scrollIntoView();", restaurantATag)

    time.sleep(rand)
    driver.implicitly_wait(rand)

    restaurantATag.click()

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(rand)
    driver.implicitly_wait(rand)

    name = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_profile .tit"))
    ).text
    location = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "locat")))
    locationArr = location.text.split("\n")[0].split(" ")
    metropolitan = locationArr[0]
    city = locationArr[1]
    district = locationArr[2]
    detailedAddress = locationArr[3]
    print("name:", name)
    print("metropolitan:", metropolitan)
    print("city:", city)
    print("district:", district)
    print("detailedAddress:", detailedAddress)
    data.append([name, metropolitan, city, district, detailedAddress])

    # Switch to the first tab
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(rand)
    driver.implicitly_wait(rand)

main = driver.window_handles
for i in main:
    driver.switch_to.window(i)
    driver.close()

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

for i in range(25):
    # delete 키 오른쪽 바로 옆에 있는 end키를 여러번 눌러서 페이지 끝까지 내린다.
    action.send_keys(
        Keys.END
    )  # 모든 데이타가 다 불러져 온 상태에서 크롤링을 하려고 끝까지 페이지를 내린거다.

action.send_keys(Keys.HOME)

read_more_elements = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "Read__More__Text"))
)
try:
    for read_more in read_more_elements:
        # driver.execute_script("arguments[0].scrollIntoView();", read_more)
        read_more.click()

        driver.switch_to.window(driver.window_handles[-1])

        restaurants = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "InfoHeader"))
        )

        for restaurant in restaurants:
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
            data.append([name, metropolitan, city, district, detailedAddress])

            # Switch to the second tab
            driver.switch_to.window(driver.window_handles[1])

        main = driver.window_handles
        for i in range(1, len(main)):  # Start from index 1 to skip the first tab
            driver.switch_to.window(main[i])
            driver.close()

        # Switch to the first second tab
        driver.switch_to.window(driver.window_handles[0])
except Exception as e:
    print("error occurred:", e)
finally:
    main = driver.window_handles
    for i in main:
        driver.switch_to.window(i)
        driver.close()

df = pd.DataFrame(
    data, columns=["name", "metropolitan", "city", "district", "detailedAddress"]
)
df.to_csv("diningcode.csv", index=False)

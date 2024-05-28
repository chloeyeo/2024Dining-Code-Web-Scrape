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
    JavascriptException,
    NoSuchElementException,
    NoSuchWindowException,
)


options = Options()
options.add_extension(
    "./extensions/ad_block.crx"
)  # using "adguard" ad blocker chrome extension - saved this as crx file
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

action.send_keys(Keys.HOME)  # goes to topmost part of page

read_more_elements = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "Read__More__Text"))
)

num_restaurants = 0

try:
    for read_more in read_more_elements[48:54]:
        print("before execute_script read_more")
        driver.execute_script("arguments[0].scrollIntoView();", read_more)
        # Click the element using JavaScript
        driver.execute_script("arguments[0].click();", read_more)
        # read_more.click()

        try:
            driver.switch_to.window(driver.window_handles[-1])
            print("Open and switch to second tab")
        except NoSuchWindowException as e:
            print("Error opening and switching to second tab:", e)
            continue  # Skip to the next iteration of the loop

        restaurants = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "InfoHeader"))
        )

        for restaurant in restaurants:
            num_restaurants += 1
            restaurant.click()

            try:
                # Switch to the newly opened tab
                driver.switch_to.window(driver.window_handles[-1])
                print("Opened and switched to restaurant tab")
            except NoSuchWindowException as e:
                print("Error opening and switching to restaurant tab:", e)
                continue  # Skip to the next iteration of the loop

            my_restaurant = {}

            name = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_profile .tit"))
            ).text
            print("name:", name)
            location = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "locat")))
            locationArr = location.text.split("\n")[0].split(" ")
            print("location:", locationArr)
            metropolitan = locationArr[0]
            city = locationArr[1]
            district = locationArr[2]
            detailedAddress = locationArr[3]
            rating = wait.until(
                EC.element_to_be_clickable((By.ID, "lbl_review_point"))
            ).text
            print("rating:", rating)

            my_restaurant["name"] = name
            # print("restaurant name:", name)
            my_restaurant["address"] = {
                "metropolitan": metropolitan,
                "city": city,
                "district": district,
                "detailedAddress": detailedAddress,
            }
            my_restaurant["rating"] = rating
            my_restaurant["menuAndPrice"] = []
            try:
                menuList = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "ul.list.Restaurant_MenuList")
                    )
                )[0]
                menuList_li_tags = menuList.find_elements(By.TAG_NAME, "li")

                for li in menuList_li_tags:
                    menu_name = li.find_element(
                        By.CSS_SELECTOR, "span.Restaurant_Menu"
                    ).text
                    price_element = li.find_element(
                        By.CLASS_NAME, "Restaurant_MenuPrice"
                    )
                    print("just before driver execute_script")
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", price_element
                    )
                    price = price_element.text
                    print("menu:", menu_name, "price:", price)
                    menu_item = {"menu": menu_name, "price": price}
                    my_restaurant["menuAndPrice"].append(menu_item)
            except:
                print("menu not found")

            my_restaurant["image"] = []

            try:
                images = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".s-list.pic-grade")
                    )
                )[0]
                img_tags = images.find_elements(By.TAG_NAME, "img")
                for img_element in img_tags:
                    src_value = img_element.get_attribute("src")
                    my_restaurant["image"].append(src_value)
                    print("img src value:", src_value)
            except:
                print("restaurant has no image")

            my_restaurant["location"] = {"type": "Point", "coordinates": []}
            my_restaurant["category"] = [{"foodType": ""}, {"mateType": []}]
            data.append(my_restaurant)

            try:
                # driver.switch_to.window(driver.window_handles[-1])
                driver.close()  # closes current tab
                print("Closed the current restaurant tab")
            except NoSuchWindowException as e:
                print("Error closing current restaurant tab:", e)
                continue  # Skip to the next iteration of the loop

            try:
                # Switch to the second tab
                driver.switch_to.window(driver.window_handles[1])
                print("Switched back to second tab")
            except NoSuchWindowException as e:
                print("Error switching back to second tab:", e)
                continue  # Skip to the next iteration of the loop

        try:
            driver.close()
            print("Closed second tab")
        except NoSuchWindowException as e:
            print("Error closing current second tab:", e)
            continue  # Skip to the next iteration of the loop

        try:
            # Switch to the first tab
            driver.switch_to.window(driver.window_handles[0])
            print("Switched back to first tab")
        except NoSuchWindowException as e:
            print("Error switching back to first tab:", e)
            continue  # Skip to the next iteration of the loop

except NoSuchElementException as e:
    print("Element not found on the page:", e)
except StaleElementReferenceException as e:
    print("Stale element reference encountered:", e)
except ElementClickInterceptedException as e:
    print("Element click intercepted:", e)
except JavascriptException as e:
    print("Javascript exception occurred:", e)
except Exception as e:
    if str(e):  # checks if exception message isn't empty
        print("error occurred:", e)
    else:  # prints out type of exception
        print("error occurred:", type(e).__name__)

print("number of restaurants printed out so far:", num_restaurants)
driver.close()

df = pd.DataFrame(data)

with open("ninth_six_sliders.json", "w", encoding="utf-8") as file:
    df.to_json(file, orient="split", force_ascii=False, index=False)

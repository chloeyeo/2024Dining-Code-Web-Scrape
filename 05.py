from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True) # stop webdriver turning off
options.add_argument("--start-maximized") # max browser screen size

service = Service()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.diningcode.com/")

# Search__Input
searchInput = driver.find_element(By.CLASS_NAME, "Search__Input")
searchInput.click()
searchInput.send_keys("분식집", Keys.ENTER)

# copy paste xpath
# //*[@id="root"]/div/main/div[2]/div[3]/ol/li[1]/a/div[1]/div/div[1]/h1
item_info = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div[3]/ol/li[1]/a/div[1]/div/div[1]/h1')
item_info.click()

data = []

wait = WebDriverWait(driver, 10)


try: 
    close_ad = wait.until(EC.visibility_of_element_located((By.ID, "dismiss-button")))
    close_ad.click()

    location = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "locat")))
    print("location:", location)

except TimeoutException:
    print("close_ad and location buttons not found within the timeout.")

# df = pd.DataFrame(data, columns=[])

# index=False otherwise first column will be named index
# df.to_csv("diningcode.csv", index=False)
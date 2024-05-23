from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True) # stop webdriver turning off
options.add_argument("--start-maximized") # max browser screen size

service = Service()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.diningcode.com/")
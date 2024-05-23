# webdriver module provides methods to initialize and control a webbrowser
from selenium import webdriver

# Service class from selenium package used for managing the ChromeDriver service.
# ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome.
from selenium.webdriver.chrome.service import Service

# Options class is used to set varius options for the Chrome Browser, e.g.
# running in headless mode, setting user preferences, etc.
from selenium.webdriver.chrome.options import Options

# ChromeDriverManager class from webdriver_manager package 
# automates the process of downloading the correct version of
# ChromeDriver and setting it up.
# To ensure the correct version of ChromeDriver is used
from webdriver_manager.chrome import ChromeDriverManager

"""
setting up the ChromeDriver service
service = Service(...) creates a new instance of the Service class
executable_path tells selenium where to find the ChromeDriver executable
ChromeDriverManager().install() automatically downloads the latest version
of ChromeDriver that is compatible with the installed version of Chrome
and returns the path to the downloaded ChromeDriver executable

ChromeDriver is a separate executable that Selenium Webdriver uses to
control Chrome. ChromeDriver acts as a bridge between the Selenium scripts
and the Chrome browser. ChromeDriver translates the commands from the
Selenium WebDriver into actions performed in the Chrome browser.

Service is a class in Selenium used to manage the lifecycle of the ChromeDriver
executable. Service handles starting and stopping the ChromeDriver process.
Use Service class to specify the executable path of ChromeDriver and any additional
configurations needed for the driver service.
""" 
service = Service(executable_path=ChromeDriverManager().install())

"""
initializing the webdriver
creates a new instance of the Chrome webdriver
using the previously set up service
this instance ('driver') is used to control the Chrome browser

webdriver is a Selenium interface used for controlling web browsers.
webdriver provides methods to perform actions such as navigating to a web page,
clicking on elements, entering text, etc.
When you create a 'webdriver.Chrome' instance, you're using webdriver to
interact with Chrome via ChromeDriver.
The 'driver' instance is what you use to interact with the web browser.
"""
driver = webdriver.Chrome(service=service)

# navigating to a website
# makes the browser controlled by the 'driver' instance (i.e. Chrome browser)
# to navigate to the specified URL
driver.get("https://www.diningcode.com/")

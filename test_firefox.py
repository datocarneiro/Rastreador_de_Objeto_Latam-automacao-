from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

options = Options()
options.add_argument("--headless")

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://google.com")
print(driver.title)
driver.quit()

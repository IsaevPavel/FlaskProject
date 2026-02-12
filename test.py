from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(r"C:\PythonProject\chromedriver.exe")  # путь к настоящему chromedriver

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.gismeteo.by/weather-minsk-4248/")
print(driver.title)  # проверка, что страница загрузилась
driver.quit()

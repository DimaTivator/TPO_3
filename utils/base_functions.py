from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.gismeteo.ru"
CITY_PATH = "/weather-sankt-peterburg-4079/"

def open_page(driver, path: str = ""):
    driver.get(BASE_URL + path)

def get_wait(driver, timeout: int = 10) -> WebDriverWait:
    return WebDriverWait(driver, timeout)

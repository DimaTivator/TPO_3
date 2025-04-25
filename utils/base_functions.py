from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.gismeteo.ru"
CITY_PATH = "/weather-sankt-peterburg-4079/"

def open_page(driver, path: str = ""):
    driver.get(BASE_URL + path)

def get_wait(driver, timeout: int = 10):
    return WebDriverWait(driver, timeout)

def check_element_exists_by_xpath(xpath: str, driver, timeout: int = 10):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except Exception:
        raise AssertionError(f"Element not found by XPath: {xpath}")

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

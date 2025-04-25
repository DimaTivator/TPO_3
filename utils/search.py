from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait


def find_search_input(wait: WebDriverWait):
    """Поиск поля input для ввода города"""
    return wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@class, 'input js-input') and @placeholder='Поиск местоположения']")
        )
    )

def search_city(wait: WebDriverWait, city_name: str):
    """Вводит город в поле поиска и нажимает enter."""
    inp = find_search_input(wait)
    inp.clear()
    inp.send_keys(city_name)
    inp.send_keys(Keys.ENTER)

def select_suggestion(wait: WebDriverWait, city_name: str):
    """Кликает по подсказке с названием города."""
    suggestion = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             f"//li[contains(@class,'group-city')]//span[text()='{city_name}']")
        )
    )
    suggestion.click()


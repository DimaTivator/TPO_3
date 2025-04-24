import pytest

from utils.base_functions import *
from utils.search import *


@pytest.mark.parametrize("city_name, expected_title", [
    ("Санкт-Петербург", "Погода в Санкт-Петербурге"),
    ("Москва", "Погода в Москве"),
    ("Казань", "Погода в Казани"),
])
def test_search_valid_city(driver, city_name, expected_title):
    wait = get_wait(driver)
    open_page(driver)
    search_city(wait, city_name)
    select_suggestion(wait, city_name)

    h1 = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//h1[contains(text(),'{expected_title}')]")
    ))
    assert expected_title in h1.text

def test_search_invalid_city(driver):
    wait = get_wait(driver)
    open_page(driver)
    search_city(wait, "asdfgh")

    error = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='search-empty']")
    ))
    assert error.is_displayed()
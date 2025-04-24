import pytest
from utils.base_functions import *
from utils.tabs import *
from utils.search import *

def test_main_elements(driver):
    """Check that all main elements of the page are loaded"""
    wait = get_wait(driver)
    open_page(driver)

    xpaths = [
        "//div[contains(@class, 'header-logo') and @data-stat-type='logo']",

        "//h1[@data-stat-type='menu' and text()='Погода']",
        "//a[@href='/news/' and text()='Новости']",
        "//a[@href='/maps/' and text()='Карты']",
        "//a[@href='/soft/' and text()='Приложения']",

        "//div[contains(@class, 'header-container') and contains(@class, 'wrap')]",
        "//input[contains(@class, 'input js-input') and @placeholder='Поиск местоположения']",
        "//div[contains(@class, 'widget') and contains(@class, 'cities-popular')]"
    ]
    for xpath in xpaths:
        check_element_exists_by_xpath(xpath, driver)


@pytest.mark.parametrize("tab_text,path", [
    ("Сейчас", CITY_PATH),
    ("По часам", CITY_PATH),
    ("Завтра", CITY_PATH),
    ("3 дня", CITY_PATH),
])
def test_tabs_navigation(driver, tab_text, path):
    wait = get_wait(driver)
    open_page(driver, path)
    click_tab(wait, tab_text)

    active = wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//div[contains(@class,'is-active') and contains(text(),'{tab_text}')]")
    ))
    assert tab_text in active.text
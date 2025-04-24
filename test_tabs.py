import pytest
from utils.base_functions import *
from utils.tabs import *
from utils.search import *

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
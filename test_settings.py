from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from utils.base_functions import *
from utils.tabs import *
from utils.search import *


def test_change_units(driver):
    """
    Тест для изменения единиц измерения:
    - первый элемент tuple: xpath-селектор select-а
    - второй: значение для select_by_value
    - третий: xpath-локатор спана с единицей измерения
    - четвертый: ожидаемая единица измерения
    """
    params = [
        ("(//select)[1]", "f", "//p[@data-key='temperature-air']//temperature-value", "°F"),
        ("(//select)[2]", "kmh", "//p[@data-key='wind']//speed-value", "км/ч"),
        ("(//select)[3]", "hpa", "//p[@data-key='pressure']//pressure-value", "гПа"),
    ]
    wait = get_wait(driver)
    open_page(driver, CITY_PATH)
    open_settings_panel(wait)

    for select_xpath, value, result_xpath, expected in params:
        sel = wait.until(EC.element_to_be_clickable((By.XPATH, select_xpath)))
        Select(sel).select_by_value(value)

    close_settings_panel(wait)

    for _, _, result_xpath, expected in params:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        assert expected in elem.text or expected in elem.get_attribute("innerText")
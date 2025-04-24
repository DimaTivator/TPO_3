from utils.base_functions import *
from utils.tabs import *
from utils.search import *

def test_forecast_filter_toggle(driver):
    wait = get_wait(driver)
    open_page(driver, CITY_PATH)

    dataset_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'js-dataset-button')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dataset_button)
    driver.execute_script("arguments[0].click();", dataset_button)

    # Скрываем heat-index, включаем pressure
    for label, should_be_on in [("Температура по ощущению", False), ("Давление", True)]:
        btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//button[@role='switch'][.//span[text()='{label}']]")
        ))
        current = btn.get_attribute("aria-checked") == "true"
        if current != should_be_on:
            driver.execute_script("arguments[0].click();", btn)

    close_settings_panel(wait)

    # Проверка фильтров
    assert not any(el.is_displayed() for el in driver.find_elements(
        By.XPATH, "//*[contains(@class, 'widget-row-chart-temperature-heat-index')]"
    )), "Heat index should be hidden"
    assert driver.find_elements(By.XPATH, "//*[contains(@data-row, 'pressure')]"), "Pressure should be visible"
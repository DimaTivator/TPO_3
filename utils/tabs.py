from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_tab(wait: WebDriverWait, tab_text: str):
    """Нажимает на вкладку меню выбора прогноза с указанным текстом."""
    tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space(text())='{tab_text}']"))
    )
    tab.click()

def open_settings_panel(wait: WebDriverWait):
    """Открывает меню настроек пользователя"""
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'unauthorized-button')]")
    ))
    btn.click()

def close_settings_panel(wait: WebDriverWait):
    """Закрывает меню настроек пользователя"""
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'drawer-close')]")
    )).click()
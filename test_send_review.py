import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.base_functions import open_page, get_wait, scroll_to_bottom


def test_send_review(driver):
    open_page(driver)
    wait = get_wait(driver)
    scroll_to_bottom(driver)

    fb_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'footer-feedback')]"
    )))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", fb_btn)
    driver.execute_script("arguments[0].click();", fb_btn)

    wait.until(EC.frame_to_be_available_and_switch_to_it((
        By.XPATH, "//iframe[@id='ue_widget' and contains(@src, 'userecho.com') and @frameborder='0']")))

    header_input = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@id='header']"
    )))
    header_input.send_keys("Отзыв")

    desc_div = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class,'ue-editor') and @contenteditable='true']"
    )))
    desc_div.click()
    desc_div.send_keys("Отзыв")

    email_input = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@id='user_email']"
    )))
    email_input.send_keys("aaa@example.com")

    input("Пожалуйста, пройдите капчу вручную в браузере и нажмите Enter, чтобы продолжить тест...")
    driver.switch_to.default_content()
    driver.switch_to.frame("ue_widget")

    submit_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class,'btn-pro') and normalize-space(text())='Отправить']"
    )))
    driver.execute_script("arguments[0].click();", submit_btn)

    confirmation = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//div[@class='module']//div[contains(@class,'offline-message-accepted') and contains(text(),'Ваше сообщение принято')]"
    )))
    assert "Ваше сообщение принято" in confirmation.text, f"Ожидали подтверждение отправки, получили: {confirmation.text}"

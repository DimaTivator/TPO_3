import pytest
from utils.base_functions import *
from utils.tabs import *
from utils.search import *

def test_main_elements(driver):
    """Проверка, что все основные элементы сайта загрузились"""
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


@pytest.mark.parametrize("menu_name, menu_path, locator", [
    ("Новости",    "/news/",  '//a[@data-stat-value="news"]'),
    ("Карты",      "/maps/",  '//a[@href="/maps/"]'),
    ("Приложения", "/soft/",  '//a[@href="/soft/"]'),
])
def test_switch_pages(driver, menu_name, menu_path, locator):
    open_page(driver, CITY_PATH)
    wait = get_wait(driver)

    link = wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
    link.click()

    wait.until(EC.url_contains(menu_path))
    assert menu_path in driver.current_url, \
        f"Ожидалось «{menu_path}» в {driver.current_url}"

    scroll_to_bottom(driver)


def test_news_sharing(driver):
    """Проверка, что работает кнопка Поделиться новостью"""
    open_page(driver, "/news/")
    wait = get_wait(driver)

    news_article_xpath = (
        '//div[@class="card-text"]'
        '/div[@class="text-title" and contains(text(),'
        '"В Санкт-Петербурге выходные будут холодными")]'
    )
    article = wait.until(EC.element_to_be_clickable((By.XPATH, news_article_xpath)))
    article.click()

    expected_url_part = "v-sankt-peterburge-vyhodnye-budut-holodnymi"
    wait.until(EC.url_contains(expected_url_part))
    assert expected_url_part in driver.current_url, "Статья не открылась"

    share_vk_xpath = '//div[@class="social-buttons"]//a[@data-stat-value="share-vk"]'
    share_vk_button = wait.until(EC.element_to_be_clickable((By.XPATH, share_vk_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", share_vk_button)
    driver.execute_script("arguments[0].click();", share_vk_button)

    driver.switch_to.window(driver.window_handles[-1])
    assert "oauth.vk.com/authorize" in driver.current_url, "Не открылась страница ВК"

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def test_map_controls_buttons_xpath(driver):
    """Проверка, что кнопки play и pause работают"""
    open_page(driver, '/maps')
    wait = get_wait(driver)

    controls = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[contains(@class, "map-controls")]')
    ))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", controls)

    pause_btn = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//button[contains(@class, "btn-pause")]')
    ))
    assert not pause_btn.is_enabled(), "Pause button should be disabled on page load"

    play_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(@class, "btn-play")]')
    ))
    assert play_btn.is_enabled(), "Play button should be enabled on page load"
    driver.execute_script("arguments[0].click();", play_btn)

    wait.until(lambda d: not play_btn.is_enabled())
    assert not play_btn.is_enabled(), "Play button should be disabled after clicking"
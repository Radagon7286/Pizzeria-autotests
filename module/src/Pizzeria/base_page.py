import logging

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url="https://pizzeria.skillbox.cc/"):
        self.driver = driver
        self.base_url = base_url
        self.actions = ActionChains(driver)

    def open(self, url=None):
        target = url or self.base_url
        logging.info(f"Открываем страницу: {target}")
        self.driver.get(target)

    def find_element(self, locator, timeout=10):
        logging.debug(f"Ищем элемент: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Не найден элемент: {locator}",
        )

    def find_elements(self, locator, timeout=10):
        """Найти все элементы. Вернуть пустой список, если ничего нет."""
        logging.debug(f"Ищем элементы: {locator}")
        return self.driver.find_elements(*locator)

    def click(self, locator, timeout=10):
        logging.info(f"Кликаем: {locator}")
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент не кликабелен: {locator}",
        )
        element.click()

    def type(self, locator, text, timeout=10):
        logging.info(f"Вводим '{text}' в {locator}")
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=10):
        text = self.find_element(locator, timeout).text
        logging.debug(f"Получен текст: {text}")
        return text

    def hover(self, locator, timeout=10):
        logging.info(f"Наводим мышь на: {locator}")
        element = self.find_element(locator, timeout)
        self.actions.move_to_element(element).perform()

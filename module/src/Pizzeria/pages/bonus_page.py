import logging

import allure

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.bonus_page_locators import BonusPageLocators


class BonusPage(BasePage):
    def __init__(self, driver, base_url="https://pizzeria.skillbox.cc/bonus/"):
        super().__init__(driver, base_url)

    @allure.step("Заполнить форму бонусной программы")
    def fill_form(self, name, phone):
        """Заполнить поля формы."""
        self.type(BonusPageLocators.NAME_INPUT, name)
        self.type(BonusPageLocators.PHONE_INPUT, phone)
        logging.info(f"Форма заполнена: name='{name}', phone='{phone}'")

    @allure.step("Нажать «Оформить карту»")
    def submit(self):
        """Нажать кнопку отправки формы."""
        self.click(BonusPageLocators.SUBMIT_BUTTON)
        logging.info("Нажата кнопка «Оформить карту»")

    @allure.step("Получить текст сообщения об ошибке")
    def get_error_message(self):
        """Вернуть текст из контейнера сообщений."""
        element = self.find_element(BonusPageLocators.MESSAGE_CONTAINER)
        return element.text.strip()

    @allure.step("Проверить, что карта оформлена")
    def is_card_created(self, timeout=10):
        """Проверить, что появилось сообщение об успехе."""
        from selenium.webdriver.support.wait import WebDriverWait

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: BonusPageLocators.SUCCESS_TEXT in
                d.find_element(*BonusPageLocators.MAIN_CONTAINER).text,
                message="Сообщение об успехе не появилось",
            )
            return True
        except Exception:
            return False

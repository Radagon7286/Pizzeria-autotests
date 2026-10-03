import logging

import allure

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.account_page_locators import AccountPageLocators


class AccountPage(BasePage):
    def __init__(
        self, driver, base_url="https://pizzeria.skillbox.cc/my-account/"
    ):
        super().__init__(driver, base_url)

    @allure.step("Открыть страницу «Мой аккаунт»")
    def open_account(self):
        self.driver.get("https://pizzeria.skillbox.cc/my-account/")

    @allure.step("Открыть страницу регистрации")
    def open_register(self):
        self.driver.get("https://pizzeria.skillbox.cc/register/")

    @allure.step("Кликнуть по кнопке «Зарегистрироваться» на /my-account/")
    def click_register_button(self):
        """Нажать кнопку, которая редиректит на /register/."""
        element = self.find_element(AccountPageLocators.REGISTER_LINK_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверить, что открыта форма регистрации")
    def is_register_form_visible(self):
        forms = self.driver.find_elements(*AccountPageLocators.REGISTER_FORM)
        if not forms:
            return False
        return forms[0].is_displayed()

    @allure.step("Зарегистрировать пользователя: {username}")
    def register(self, username, email, password):
        """Заполнить форму регистрации и отправить."""
        self.type(AccountPageLocators.REGISTER_USERNAME, username)
        self.type(AccountPageLocators.REGISTER_EMAIL, email)
        self.type(AccountPageLocators.REGISTER_PASSWORD, password)
        self.click(AccountPageLocators.REGISTER_BUTTON)
        logging.info(f"Регистрация отправлена: {username}")

    @allure.step("Войти как {username}")
    def login(self, username, password):
        """Войти через форму на /my-account/."""
        self.type(AccountPageLocators.LOGIN_USERNAME, username)
        self.type(AccountPageLocators.LOGIN_PASSWORD, password)
        self.click(AccountPageLocators.LOGIN_BUTTON)
        logging.info(f"Вход выполнен: {username}")

    @allure.step("Проверить, что пользователь залогинен")
    def is_logged_in(self):
        """Проверить, что на странице есть блок личного кабинета."""
        blocks = self.driver.find_elements(*AccountPageLocators.ACCOUNT_CONTENT)
        return bool(blocks and blocks[0].is_displayed())

    @allure.step("Проверить, что регистрация прошла успешно")
    def is_registration_successful(self):
        """Проверить, что на странице есть сообщение об успешной регистрации."""
        messages = self.driver.find_elements(
            *AccountPageLocators.REGISTER_SUCCESS_MESSAGE
        )
        if messages:
            logging.info(f"Найдено сообщение: '{messages[0].text}'")
            return True
        return False

import logging

import allure

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.checkout_page_locators import CheckoutPageLocators


class CheckoutPage(BasePage):
    def __init__(self, driver, base_url="https://pizzeria.skillbox.cc/checkout/"):
        super().__init__(driver, base_url)

    @allure.step("Получить заголовок страницы оформления")
    def get_page_title(self):
        title = self.get_text(CheckoutPageLocators.PAGE_TITLE)
        logging.info(f"Заголовок: {title}")
        return title

    @allure.step("Проверить, что требуется авторизация")
    def is_login_required(self):
        """Вернуть True, если на странице есть сообщение об авторизации."""
        messages = self.driver.find_elements(
            *CheckoutPageLocators.LOGIN_REQUIRED_MESSAGE
        )
        for msg in messages:
            if "авторизоваться" in msg.text.lower() or "авторизуйтесь" in msg.text.lower():
                logging.info(f"Найдено сообщение: '{msg.text}'")
                return True
        return False

    @allure.step("Кликнуть по ссылке «Авторизуйтесь»")
    def click_login_link(self):
        self.click(CheckoutPageLocators.LOGIN_LINK)

    @allure.step("Заполнить данные доставки")
    def fill_delivery_data(
            self,
            first_name,
            last_name,
            address,
            city,
            state,
            postcode,
            phone,
            order_date,
            comments="",
    ):
        """Заполнить форму доставки."""
        self.type(CheckoutPageLocators.FIRST_NAME, first_name)
        self.type(CheckoutPageLocators.LAST_NAME, last_name)
        self.type(CheckoutPageLocators.ADDRESS, address)
        self.type(CheckoutPageLocators.CITY, city)
        self.type(CheckoutPageLocators.STATE, state)
        self.type(CheckoutPageLocators.POSTCODE, postcode)
        self.type(CheckoutPageLocators.PHONE, phone)

        # Дата доставки: поле type="date" требует формат YYYY-MM-DD
        date_field = self.find_element(CheckoutPageLocators.ORDER_DATE)
        self.driver.execute_script(
            f"arguments[0].value = '{order_date}';", date_field
        )

        if comments:
            self.type(CheckoutPageLocators.ORDER_COMMENTS, comments)

        logging.info(f"Данные доставки заполнены: {first_name} {last_name}")

    @allure.step("Выбрать оплату при доставке")
    def select_payment_cod(self):
        """Выбрать оплату при доставке."""
        element = self.find_element(CheckoutPageLocators.PAYMENT_COD)
        self.driver.execute_script("arguments[0].click();", element)
        logging.info("Выбрана оплата: при доставке")

    @allure.step("Принять условия")
    def accept_terms(self):
        """Поставить галочку согласия с условиями."""
        checkbox = self.find_element(CheckoutPageLocators.TERMS_CHECKBOX)
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)
            logging.info("Условия приняты")

    @allure.step("Подтвердить заказ")
    def place_order(self):
        """Нажать кнопку «Оформить заказ» через JS (обход перекрытия)."""
        button = self.find_element(CheckoutPageLocators.PLACE_ORDER_BUTTON)
        logging.info("Подтверждаем заказ (JS-клик)")

        # Скроллим к кнопке
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )

        # Кликаем через JS — игнорирует перекрытие
        self.driver.execute_script("arguments[0].click();", button)
        logging.info("Кнопка «Оформить заказ» нажата")

    @allure.step("Проверить, что заказ оформлен")
    def is_order_received(self):
        """Проверить, что показано сообщение об успешном заказе."""
        elements = self.driver.find_elements(
            *CheckoutPageLocators.ORDER_RECEIVED
        )
        return bool(elements and elements[0].is_displayed())

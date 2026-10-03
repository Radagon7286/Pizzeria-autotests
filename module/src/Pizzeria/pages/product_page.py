import logging

import allure
from selenium.webdriver.support.ui import Select

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.product_page_locators import ProductPageLocators


class ProductPage(BasePage):
    def __init__(self, driver, base_url="https://pizzeria.skillbox.cc/"):
        super().__init__(driver, base_url)

    @allure.step("Получить название товара")
    def get_title(self):
        title = self.get_text(ProductPageLocators.PRODUCT_TITLE)
        logging.info(f"Название товара: {title}")
        return title

    @allure.step("Получить цену товара")
    def get_price(self):
        price = self.get_text(ProductPageLocators.PRODUCT_PRICE)
        logging.info(f"Цена товара: {price}")
        return price

    @allure.step("Выбрать борт: {board}")
    def select_board(self, board):
        """Выбрать борт в дропдауне по visible text."""
        select = Select(self.find_element(ProductPageLocators.BOARD_PACK_SELECT))
        select.select_by_visible_text(board)
        logging.info(f"Выбран борт: {board}")

    @allure.step("Выбрать борт по value: {value}")
    def select_board_by_value(self, value):
        """Выбрать борт в дропдауне по value опции."""
        select = Select(self.find_element(ProductPageLocators.BOARD_PACK_SELECT))
        select.select_by_value(value)
        logging.info(f"Выбран борт с value: {value}")

    @allure.step("Получить выбранный борт")
    def get_selected_board(self):
        """Вернуть текст выбранной опции борта."""
        select = Select(self.find_element(ProductPageLocators.BOARD_PACK_SELECT))
        selected = select.first_selected_option.text
        logging.info(f"Выбранный борт: {selected}")
        return selected

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        self.click(ProductPageLocators.ADD_TO_CART_BUTTON)

    @allure.step("Получить URL текущей страницы")
    def get_url(self):
        return self.driver.current_url

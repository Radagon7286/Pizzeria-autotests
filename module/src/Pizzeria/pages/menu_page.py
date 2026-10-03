import logging

import allure

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.menu_page_locators import MenuPageLocators


class MenuPage(BasePage):
    def __init__(
        self,
        driver,
        base_url="https://pizzeria.skillbox.cc/product-category/menu/deserts/",
    ):
        super().__init__(driver, base_url)

    @allure.step("Получить заголовок страницы")
    def get_page_title(self):
        title = self.get_text(MenuPageLocators.PAGE_TITLE)
        logging.info(f"Заголовок: {title}")
        return title

    @allure.step("Получить количество товаров на странице")
    def get_products_count(self):
        items = self.driver.find_elements(*MenuPageLocators.PRODUCT_ITEM)
        logging.info(f"Товаров на странице: {len(items)}")
        return len(items)

    @allure.step("Получить названия всех товаров")
    def get_product_titles(self):
        titles = [
            el.text for el in
            self.driver.find_elements(*MenuPageLocators.PRODUCT_TITLE)
        ]
        logging.info(f"Названия: {titles}")
        return titles

    @allure.step("Получить цены всех товаров")
    def get_product_prices(self):
        prices = [
            el.text for el in
            self.driver.find_elements(*MenuPageLocators.PRODUCT_PRICE)
        ]
        logging.info(f"Цены: {prices}")
        return prices

    @allure.step("Отфильтровать по максимальной цене: {max_price}")
    def filter_by_max_price(self, max_price, min_price=110):
        """Открыть URL с фильтром по цене через GET-параметры."""
        url = f"{self.base_url}?min_price={min_price}&max_price={max_price}"
        logging.info(f"Открываем URL с фильтром: {url}")
        self.driver.get(url)

    @allure.step("Добавить товар #{index} в корзину")
    def add_product_to_cart(self, index=0):
        buttons = self.find_elements(MenuPageLocators.PRODUCT_ADD_TO_CART)
        button = buttons[index]
        logging.info(f"Добавляем товар #{index} в корзину")
        # Скроллим к кнопке
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        # Кликаем через JS (кнопка может быть перекрыта)
        self.driver.execute_script("arguments[0].click();", button)

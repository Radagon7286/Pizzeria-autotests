import logging

import allure

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.cart_page_locators import CartPageLocators


class CartPage(BasePage):
    def __init__(self, driver, base_url="https://pizzeria.skillbox.cc/cart/"):
        super().__init__(driver, base_url)

    @allure.step("Получить количество позиций в корзине")
    def get_items_count(self):
        items = self.find_elements(CartPageLocators.CART_ITEM)
        logging.info(f"Позиций в корзине: {len(items)}")
        return len(items)

    @allure.step("Получить названия всех товаров в корзине")
    def get_item_names(self):
        names = [
            el.text for el in self.find_elements(CartPageLocators.ITEM_NAME)
        ]
        logging.info(f"Товары в корзине: {names}")
        return names

    @allure.step("Изменить количество товара #{index} на {qty}")
    def change_quantity(self, index, qty):
        """Изменить количество товара по индексу."""
        fields = self.find_elements(CartPageLocators.ITEM_QUANTITY)
        field = fields[index]
        field.clear()
        field.send_keys(str(qty))
        logging.info(f"Количество товара #{index} изменено на {qty}")

    @allure.step("Нажать «Обновить корзину»")
    def click_update_cart(self):
        """Кликнуть по кнопке «Обновить корзину» и дождаться перезагрузки."""
        import time

        button = self.find_element(CartPageLocators.UPDATE_CART_BUTTON)

        # Снимаем disabled, если он есть
        self.driver.execute_script(
            "arguments[0].removeAttribute('disabled');", button
        )

        # Скроллим к кнопке (чтобы не перекрывалась другими элементами)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        time.sleep(0.3)

        # Настоящий клик
        button.click()
        logging.info("Кликнули по кнопке «Обновить корзину»")

        # Ждём, что страница перезагрузится
        time.sleep(2)

    @allure.step("Удалить товар #{index} из корзины")
    def remove_item(self, index=0):
        """Удалить товар из корзины и дождаться перезагрузки."""
        from selenium.webdriver.support.wait import WebDriverWait

        # Считаем ДО удаления
        count_before = len(self.driver.find_elements(*CartPageLocators.CART_ITEM))
        logging.info(f"Позиций до удаления: {count_before}")

        if count_before == 0:
            logging.info("Корзина уже пуста")
            return

        buttons = self.find_elements(CartPageLocators.ITEM_REMOVE)
        button = buttons[index]

        # Скроллим и кликаем
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        button.click()
        logging.info("Кликнули по крестику удаления")

        # Ждём, что количество стало МЕНЬШЕ
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*CartPageLocators.CART_ITEM)) < count_before,
            message="Товар не удалился",
        )
        logging.info("Товар удалён")

    @allure.step("Перейти к оформлению заказа")
    def go_to_checkout(self):
        self.click(CartPageLocators.CHECKOUT_BUTTON)

    @allure.step("Применить купон: {code}")
    def apply_coupon(self, code):
        """Ввести код купона и нажать «Применить купон»."""
        self.type(CartPageLocators.COUPON_INPUT, code)
        self.click(CartPageLocators.APPLY_COUPON_BUTTON)
        logging.info(f"Купон '{code}' применён")
        import time
        time.sleep(1.5)

    @allure.step("Получить итоговую сумму корзины")
    def get_total(self):
        """Вернуть итоговую сумму корзины."""
        total = self.get_text(CartPageLocators.CART_TOTAL)
        logging.info(f"Итоговая сумма: {total}")
        return total

    @allure.step("Получить размер скидки")
    def get_discount(self):
        """Вернуть размер скидки из строки купона."""
        if not self.driver.find_elements(*CartPageLocators.COUPON_ROW):
            return None
        amount = self.get_text(CartPageLocators.COUPON_AMOUNT)
        logging.info(f"Скидка: {amount}")
        return amount

    @allure.step("Проверить, что купон применён")
    def is_coupon_applied(self):
        """Проверить, что строка купона появилась в сводке."""
        from selenium.webdriver.support.wait import WebDriverWait
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(*CartPageLocators.COUPON_ROW)) > 0,
                message="Строка купона не появилась",
            )
            logging.info("Купон применён (строка найдена)")
            return True
        except Exception:
            logging.info("Купон не применён (строка не найдена)")
            return False

    @allure.step("Удалить все применённые купоны")
    def remove_all_coupons(self):
        """Удалить все купоны из корзины."""
        import time

        while True:
            buttons = self.driver.find_elements(*CartPageLocators.REMOVE_COUPON)
            if not buttons:
                break
            logging.info(f"Удаляем купон, осталось: {len(buttons)}")
            buttons[0].click()
            time.sleep(1.5)
        logging.info("Все купоны удалены")

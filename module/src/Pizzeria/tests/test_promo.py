import logging
import re

import allure
import pytest

from module.src.Pizzeria.pages.main_page import MainPage
from module.src.Pizzeria.pages.cart_page import CartPage


@allure.feature("Промокоды")
class TestPromo:

    @pytest.fixture(autouse=True)
    def setup_cart(self, selenium):
        """Перед каждым тестом: логин + чистая корзина + пицца + удаление купонов."""
        from module.src.Pizzeria.pages.account_page import AccountPage

        # Логин
        account_page = AccountPage(selenium)
        account_page.open_account()
        account_page.login(username="test777test", password="qwertyqwer")

        # 1. Чистим корзину
        main_page = MainPage(selenium)
        main_page.open()
        main_page.go_to_cart()
        cart_page = CartPage(selenium)

        while cart_page.get_items_count() > 0:
            cart_page.remove_item(index=0)

        # 2. Удаляем купоны, если остались
        cart_page.remove_all_coupons()

        # 3. Добавляем пиццу за 435₽
        main_page.open()
        main_page.add_pizza_and_wait(index=0)
        main_page.go_to_cart()

        # 4. ЕЩЁ РАЗ удаляем купоны — теперь они точно есть и видны
        cart_page.remove_all_coupons()

        yield

    def _parse_amount(self, text):
        """Извлечь число из строки вида '391,50₽' или '-43,50₽'."""
        numbers = re.findall(r"-?\d+[,.]?\d*", text.replace(" ", ""))
        if not numbers:
            return 0.0
        return float(numbers[0].replace(",", "."))

    @allure.story("Промокод")
    @allure.title("Применение промокода GIVEMEHALYAVA — скидка 10%")
    def test_promo_valid(self, selenium):
        cart_page = CartPage(selenium)

        with allure.step("Запоминаем сумму до применения купона"):
            total_before = self._parse_amount(cart_page.get_total())
            logging.info(f"Сумма до: {total_before}")

        with allure.step("Применяем купон GIVEMEHALYAVA"):
            cart_page.apply_coupon("GIVEMEHALYAVA")

        with allure.step("Проверяем, что купон применился"):
            assert cart_page.is_coupon_applied(), "Купон не применился"

        with allure.step("Проверяем, что скидка 10%"):
            total_after = self._parse_amount(cart_page.get_total())
            expected = total_before * 0.9
            logging.info(f"Сумма после: {total_after}, ожидалось: {expected}")
            assert abs(total_after - expected) < 1, (
                f"Скидка не 10%: было {total_before}, стало {total_after}"
            )

    @allure.story("Промокод")
    @allure.title("Промокод DC120 не применяется")
    def test_promo_invalid(self, selenium):
        cart_page = CartPage(selenium)

        with allure.step("Запоминаем сумму до применения купона"):
            total_before = self._parse_amount(cart_page.get_total())
            logging.info(f"Сумма до: {total_before}")

        with allure.step("Применяем купон DC120"):
            cart_page.apply_coupon("DC120")

        with allure.step("Проверяем, что купон НЕ применился"):
            assert not cart_page.is_coupon_applied(), (
                "Невалидный купон DC120 применился"
            )

        with allure.step("Проверяем, что сумма не изменилась"):
            total_after = self._parse_amount(cart_page.get_total())
            logging.info(f"Сумма после: {total_after}")
            assert total_after == total_before, (
                f"Сумма изменилась: {total_before} → {total_after}"
            )

    @pytest.mark.xfail(
        reason="Баг: промокод GIVEMEHALYAVA применяется повторно"
    )
    @allure.story("Промокод")
    @allure.title("Промокод GIVEMEHALYAVA работает только один раз")
    def test_promo_only_once(self, selenium):
        """Проверяем, что промокод применяется только к первому заказу."""
        from module.src.Pizzeria.pages.checkout_page import CheckoutPage
        from module.src.Pizzeria.pages.main_page import MainPage
        from module.src.Pizzeria.pages.cart_page import CartPage
        main_page = MainPage(selenium)
        cart_page = CartPage(selenium)
        checkout_page = CheckoutPage(selenium)
        with allure.step("Оформляем первый заказ с промокодом"):
            # setup_cart уже добавил пиццу — переходим к оформлению
            cart_page.apply_coupon("GIVEMEHALYAVA")
            assert cart_page.is_coupon_applied(), "Первый раз купон не применился"
            # Переходим к оформлению
            cart_page.go_to_checkout()
            checkout_page.fill_delivery_data(
                first_name="Олег",
                last_name="Олегович",
                address="Пушкина 44",
                city="Москва",
                state="Московская",
                postcode="101000",
                phone="+79991234567",
                order_date="2026-10-06",
            )
            checkout_page.select_payment_cod()
            checkout_page.accept_terms()
            checkout_page.place_order()
            # Ждём подтверждения
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 15).until(
                lambda d: checkout_page.is_order_received(),
                message="Первый заказ не оформлен",
            )
            logging.info("Первый заказ оформлен")

        with allure.step("Добавляем товар во вторую корзину"):
            main_page.open()
            main_page.add_pizza_and_wait(index=0)
            main_page.go_to_cart()

        with allure.step("Пробуем применить тот же промокод второй раз"):
            cart_page.apply_coupon("GIVEMEHALYAVA")

        with allure.step("Проверяем, что промокод НЕ применился"):
            applied = cart_page.is_coupon_applied()
            logging.info(f"Купон применён второй раз: {applied}")
            assert not applied, (
                "БАГ: промокод GIVEMEHALYAVA применился повторно для пользователя"
            )

    @allure.story("Промокод")
    @allure.title("Применение промокода при ошибке сервера (блокировка запроса)")
    def test_promo_server_error(self, selenium):
        """Промокод не применяется, если запрос к серверу заблокирован."""
        from module.src.Pizzeria.pages.cart_page import CartPage

        cart_page = CartPage(selenium)

        with allure.step("Запоминаем сумму до применения купона"):
            total_before = self._parse_amount(cart_page.get_total())
            logging.info(f"Сумма до: {total_before}")

        with allure.step("Блокируем запрос apply_coupon через CDP"):
            selenium.execute_cdp_cmd("Network.enable", {})
            selenium.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {"urls": ["*/?wc-ajax=apply_coupon*"]},
            )
            logging.info("Запрос apply_coupon заблокирован")

        with allure.step("Пробуем применить купон GIVEMEHALYAVA"):
            cart_page.apply_coupon("GIVEMEHALYAVA")

        with allure.step("Проверяем, что купон НЕ применился"):
            applied = cart_page.is_coupon_applied()
            logging.info(f"Купон применился: {applied}")
            assert not applied, (
                "Купон применился, хотя запрос был заблокирован"
            )

        with allure.step("Проверяем, что сумма не изменилась"):
            total_after = self._parse_amount(cart_page.get_total())
            logging.info(f"Сумма после: {total_after}")
            assert total_after == total_before, (
                f"Сумма изменилась: {total_before} → {total_after}"
            )

        with allure.step("Убираем блокировку (cleanup)"):
            selenium.execute_cdp_cmd(
                "Network.setBlockedURLs", {"urls": []}
            )
            logging.info("Блокировка снята")

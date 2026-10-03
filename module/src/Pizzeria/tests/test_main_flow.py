import allure
import logging


from module.src.Pizzeria.locators.cart_page_locators import CartPageLocators
from module.src.Pizzeria.pages.main_page import MainPage


@allure.feature("Основной флоу")
@allure.story("Главная страница")
class TestMainFlow:

    @allure.story("Главная страница")
    @allure.title("Отображение слайдера с пиццами")
    def test_slider_displayed(self, selenium):
        page = MainPage(selenium)

        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Проверяем, что слайдер отображается"):
            assert page.is_slider_displayed(), "Слайдер не отображается на странице"

        with allure.step("Проверяем, что в слайдере есть пиццы"):
            slides_count = page.get_slides_count()
            logging.info(f"Количество слайдов: {slides_count}")
            assert slides_count > 0, "В слайдере нет пицц"

    @allure.story("Слайдер")
    @allure.title("Переключение слайдера вправо")
    def test_slider_next(self, selenium):
        page = MainPage(selenium)
        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Запоминаем исходный сдвиг слайдера"):
            offset_before = page.get_slider_offset()

        with allure.step("Переключаем слайдер вправо"):
            page.click_slider_next()

        with allure.step("Проверяем, что слайдер сдвинулся"):
            offset_after = page.get_slider_offset()
            assert offset_after < offset_before, (
                f"Слайдер должен был сдвинуться вперёд (X уменьшиться): "
                f"было {offset_before}, стало {offset_after}"
            )

    @allure.story("Слайдер")
    @allure.title("Переключение слайдера влево")
    def test_slider_prev(self, selenium):
        page = MainPage(selenium)
        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Сначала сдвигаем слайдер вправо"):
            page.click_slider_next()

        with allure.step("Запоминаем сдвиг после движения вправо"):
            offset_before = page.get_slider_offset()
            logging.info(f"Сдвиг до клика влево: {offset_before}")

        with allure.step("Переключаем слайдер влево"):
            page.click_slider_prev()

        with allure.step("Проверяем, что слайдер сдвинулся назад"):
            offset_after = page.get_slider_offset()
            logging.info(f"Сдвиг после клика влево: {offset_after}")
            assert offset_after > offset_before, (
                f"Слайдер должен был сдвинуться назад (X увеличиться): "
                f"было {offset_before}, стало {offset_after}"
            )

    @allure.story("Главная")
    @allure.title("Отображение кнопки «В корзину» при наведении")
    def test_hover_shows_button(self, selenium):
        page = MainPage(selenium)

        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Проверяем, что до наведения кнопка прозрачна (opacity=0)"):
            opacity_before = page.get_button_opacity(index=0)
            logging.info(f"Opacity до hover: {opacity_before}")
            assert opacity_before == "0", (
                f"Кнопка должна быть скрыта до наведения, но opacity={opacity_before}"
            )

        with allure.step("Наводим курсор на пиццу"):
            page.hover_pizza(index=0)

        with allure.step("Проверяем, что после наведения кнопка видна (opacity=1)"):
            opacity_after = page.get_button_opacity(index=0)
            logging.info(f"Opacity после hover: {opacity_after}")
            assert opacity_after == "1", (
                f"Кнопка не появилась после наведения, opacity={opacity_after}"
            )

    @allure.story("Корзина")
    @allure.title("Добавление пиццы в корзину из слайдера")
    def test_add_pizza_to_cart(self, selenium):
        page = MainPage(selenium)

        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Запоминаем текст корзины до добавления"):
            total_before = page.get_cart_total()
            logging.info(f"Текст корзины до: '{total_before}'")

        with allure.step("Добавляем первую пиццу в корзину"):
            page.add_pizza_to_cart(index=0)

        with allure.step("Ждём обновления счётчика корзины"):
            total_after = page.wait_cart_total_changed(total_before)
            logging.info(f"Текст корзины после: '{total_after}'")

        with allure.step("Проверяем, что корзина не пустая"):
            assert "0,00" not in total_after, (
                f"Корзина осталась пустой: '{total_after}'"
            )

    @allure.story("Корзина")
    @allure.title("Добавление нескольких пицц из слайдера")
    def test_add_multiple_pizzas(self, selenium):
        page = MainPage(selenium)

        with allure.step("Открываем главную страницу"):
            page.open()

        with allure.step("Запоминаем исходный текст корзины"):
            total_start = page.get_cart_total()
            logging.info(f"Стартовый текст корзины: '{total_start}'")

        with allure.step("Добавляем первую пиццу в корзину"):
            page.add_pizza_to_cart(index=0)

        with allure.step("Ждём обновления корзины после первой пиццы"):
            total_after_first = page.wait_cart_total_changed(total_start)
            logging.info(f"После первой пиццы: '{total_after_first}'")

        with allure.step("Листаем слайдер, чтобы выбрать другую пиццу"):
            page.click_slider_next()

        with allure.step("Добавляем вторую пиццу в корзину"):
            page.add_pizza_to_cart(index=0)

        with allure.step("Ждём обновления корзины после второй пиццы"):
            total_after_second = page.wait_cart_total_changed(total_after_first)
            logging.info(f"После второй пиццы: '{total_after_second}'")

        with allure.step("Проверяем, что в корзине две разные пиццы"):
            assert total_after_first != total_after_second, (
                f"Вторая пицца не добавилась: "
                f"было '{total_after_first}', стало '{total_after_second}'"
            )

    @allure.story("Страница пиццы")
    @allure.title("Добавление пиццы с дополнительной опцией в корзину")
    def test_add_pizza_with_option(self, selenium):
        from module.src.Pizzeria.pages.product_page import ProductPage

        main_page = MainPage(selenium)
        main_page.open()

        with allure.step("Запоминаем исходный текст корзины"):
            total_before = main_page.get_cart_total()

        with allure.step("Переходим на страницу пиццы"):
            main_page.click_pizza_image(index=0)

        product_page = ProductPage(selenium)

        with allure.step("Выбираем «Сырный» борт"):
            product_page.select_board("Сырный - 55.00 р.")

        with allure.step("Добавляем в корзину"):
            product_page.add_to_cart()

        with allure.step("Ждём обновления корзины"):
            main_page.wait_cart_total_changed(total_before)
            total_after = main_page.get_cart_total()
            logging.info(f"Корзина после: '{total_after}'")
            with allure.step("Проверяем, что корзина не пустая"):
                assert total_after.strip() != "[ 0,00₽ ]", (
                    f"Корзина осталась пустой: '{total_after}'"
                )

    @allure.story("Страница пиццы")
    @allure.title("Выбор дополнительной опции «Сырный борт»")
    def test_select_cheese_border(self, selenium):
        from module.src.Pizzeria.pages.product_page import ProductPage

        main_page = MainPage(selenium)

        with allure.step("Открываем главную страницу"):
            main_page.open()

        with allure.step("Переходим на страницу пиццы"):
            main_page.click_pizza_image(index=0)

        product_page = ProductPage(selenium)

        with allure.step("Выбираем «Сырный - 55.00 р.»"):
            product_page.select_board("Сырный - 55.00 р.")

        with allure.step("Проверяем, что выбран именно «Сырный» борт"):
            selected = product_page.get_selected_board()
            logging.info(f"Выбранный борт: {selected}")
            assert "Сырный" in selected, (
                f"Выбран не тот борт: '{selected}'"
            )

    @allure.story("Корзина")
    @allure.title("Проверка содержимого корзины")
    def test_cart_content(self, selenium):
        from module.src.Pizzeria.pages.cart_page import CartPage

        main_page = MainPage(selenium)
        main_page.open()
        main_page.add_pizza_and_wait(index=0)
        main_page.go_to_cart()

        cart_page = CartPage(selenium)

        with allure.step("Проверяем, что в корзине одна позиция"):
            count = cart_page.get_items_count()
            logging.info(f"Позиций в корзине: {count}")
            assert count == 1, f"Ожидалась 1 позиция, найдено {count}"

        with allure.step("Проверяем, что название товара не пустое"):
            names = cart_page.get_item_names()
            logging.info(f"Товары: {names}")
            assert len(names) == 1
            assert "Пицца" in names[0], f"Неожиданное название: {names[0]}"

    @allure.story("Корзина")
    @allure.title("Изменение количества пиццы в корзине")
    def test_change_quantity(self, selenium):
        from module.src.Pizzeria.pages.cart_page import CartPage
        from selenium.webdriver.common.by import By

        main_page = MainPage(selenium)
        main_page.open()
        main_page.add_pizza_and_wait(index=0)
        main_page.go_to_cart()

        cart_page = CartPage(selenium)

        with allure.step("Запоминаем итог до изменения"):
            total_before = cart_page.get_total()
            logging.info(f"Итог до: '{total_before}'")

        with allure.step("Меняем количество на 2"):
            cart_page.change_quantity(index=0, qty=2)

        with allure.step("Проверяем, что поле стало 2"):
            field = selenium.find_element(
                By.CSS_SELECTOR, "td.product-quantity input.qty"
            )
            value = field.get_attribute("value")
            logging.info(f"Значение поля количества: '{value}'")
            assert value == "2", f"Количество не изменилось: '{value}'"

        with allure.step("Нажимаем «Обновить корзину»"):
            cart_page.click_update_cart()

        with allure.step("Проверяем, что итог изменился"):
            total_after = cart_page.get_total()
            logging.info(f"Итог после: '{total_after}'")
            assert total_after != total_before, (
                f"Итог не изменился: было '{total_before}', стало '{total_after}'"
            )

    @allure.story("Корзина")
    @allure.title("Удаление пиццы из корзины")
    def test_remove_from_cart(self, selenium):
        from module.src.Pizzeria.pages.cart_page import CartPage

        main_page = MainPage(selenium)
        main_page.open()
        main_page.add_pizza_and_wait(index=0)
        main_page.go_to_cart()

        cart_page = CartPage(selenium)

        with allure.step("Проверяем, что в корзине 1 позиция"):
            assert cart_page.get_items_count() == 1

        with allure.step("Удаляем товар"):
            cart_page.remove_item(index=0)

        with allure.step("Проверяем, что корзина пуста"):
            # после удаления страница перезагружается, ждём
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 10).until(
                lambda d: len(d.find_elements(
                    *CartPageLocators.CART_ITEM
                )) == 0,
                message="Корзина не очистилась после удаления",
            )
            count = cart_page.get_items_count()
            logging.info(f"Позиций после удаления: {count}")
            assert count == 0, f"Корзина не пуста, позиций: {count}"

    @allure.story("Меню")
    @allure.title("Переход в раздел меню из корзины")
    def test_go_to_menu_from_cart(self, selenium):
        main_page = MainPage(selenium)
        main_page.open()
        main_page.go_to_cart()
        main_page.go_to_menu()
        with allure.step("Проверяем, что открылся раздел меню"):
            logging.info(f"URL: {selenium.current_url}")
            assert "/product-category/menu/" in selenium.current_url, (
                f"Открылся не раздел меню: {selenium.current_url}"
            )

    @allure.story("Меню")
    @allure.title("Выбор раздела «Десерты»")
    def test_select_desserts(self, selenium):
        main_page = MainPage(selenium)
        main_page.open()

        with allure.step("Открываем страницу десертов напрямую"):
            selenium.get(
                "https://pizzeria.skillbox.cc/product-category/menu/deserts/"
            )

        with allure.step("Проверяем, что на странице десерты"):
            from module.src.Pizzeria.pages.menu_page import MenuPage
            menu_page = MenuPage(selenium)
            title = menu_page.get_page_title()
            logging.info(f"Заголовок: {title}")
            assert "ДЕСЕРТЫ" in title.upper(), (
                f"Открылась не страница десертов: '{title}'"
            )

            prices = menu_page.get_product_prices()
            logging.info(f"Цены на странице: {prices}")
            assert len(prices) > 0, "На странице нет товаров"

    @allure.story("Меню")
    @allure.title("Фильтрация десертов по цене до 135 рублей")
    def test_filter_desserts_by_price(self, selenium):
        import re
        from module.src.Pizzeria.pages.menu_page import MenuPage

        menu_page = MenuPage(selenium)
        menu_page.open()

        with allure.step("Проверяем, что до фильтра 3 десерта"):
            count_before = menu_page.get_products_count()
            logging.info(f"Десертов до фильтра: {count_before}")
            assert count_before == 3, f"Ожидалось 3 десерта, найдено {count_before}"

        with allure.step("Применяем фильтр до 135 рублей"):
            menu_page.filter_by_max_price(max_price=135)

        with allure.step("Проверяем, что осталось 2 десерта"):
            count_after = menu_page.get_products_count()
            logging.info(f"Десертов после фильтра: {count_after}")
            assert count_after == 2, (
                f"Ожидалось 2 десерта, найдено {count_after}"
            )

        with allure.step("Проверяем, что все цены не больше 135₽"):
            prices_text = menu_page.get_product_prices()
            logging.info(f"Цены после фильтра: {prices_text}")
            prices = []
            for p in prices_text:
                match = re.search(r"(\d+)[,.]?(\d*)", p.replace(" ", ""))
                if match:
                    whole = match.group(1)
                    frac = match.group(2) or "0"
                    prices.append(float(f"{whole}.{frac}"))
            logging.info(f"Числовые цены: {prices}")
            assert all(p <= 135 for p in prices), (
                f"Найдены десерты дороже 135₽: {prices}"
            )

    @allure.story("Меню")
    @allure.title("Добавление десерта в корзину")
    def test_add_dessert_to_cart(self, selenium):
        from module.src.Pizzeria.pages.menu_page import MenuPage
        from module.src.Pizzeria.pages.main_page import MainPage

        menu_page = MenuPage(selenium)
        menu_page.open()

        main_page = MainPage(selenium)

        with allure.step("Запоминаем текст корзины до добавления"):
            total_before = main_page.get_cart_total()
            logging.info(f"Корзина до: '{total_before}'")

        with allure.step("Добавляем десерт «Булочка с корицей» в корзину"):
            menu_page.add_product_to_cart(index=0)

        with allure.step("Ждём обновления корзины"):
            total_after = main_page.wait_cart_total_changed(total_before)
            logging.info(f"Корзина после: '{total_after}'")
            assert "115" in total_after, (
                f"Ожидалась сумма 115₽ (Булочка с корицей), получено: '{total_after}'"
            )

    @allure.story("Оформление заказа")
    @allure.title("Переход к оформлению неавторизованным пользователем")
    def test_checkout_unauthorized(self, selenium):
        from module.src.Pizzeria.pages.checkout_page import CheckoutPage
        from module.src.Pizzeria.pages.cart_page import CartPage

        main_page = MainPage(selenium)
        main_page.open()
        main_page.add_pizza_and_wait(index=0)
        main_page.go_to_cart()

        with allure.step("Переходим к оформлению заказа"):
            cart_page = CartPage(selenium)
            cart_page.go_to_checkout()

        with allure.step("Проверяем, что на странице оформления"):
            logging.info(f"URL: {selenium.current_url}")
            assert "/checkout/" in selenium.current_url, (
                f"Открылась не страница оформления: {selenium.current_url}"
            )

        with allure.step("Проверяем, что требуется авторизация"):
            checkout_page = CheckoutPage(selenium)
            assert checkout_page.is_login_required(), (
                "Нет сообщения о необходимости авторизации"
            )

    @allure.story("Регистрация")
    @allure.title("Переход к регистрации через «Мой аккаунт»")
    def test_go_to_registration(self, selenium):
        from module.src.Pizzeria.pages.account_page import AccountPage

        account_page = AccountPage(selenium)

        with allure.step("Открываем страницу «Мой аккаунт»"):
            account_page.open_account()

        with allure.step("Проверяем, что открылась страница аккаунта"):
            logging.info(f"URL: {selenium.current_url}")
            assert "/my-account/" in selenium.current_url, (
                f"Открылась не страница аккаунта: {selenium.current_url}"
            )

        with allure.step("Кликаем по кнопке «Зарегистрироваться»"):
            account_page.click_register_button()

        with allure.step("Проверяем, что открылась форма регистрации"):
            # Ждём перехода на /register/
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 10).until(
                lambda d: "/register/" in d.current_url,
                message="Не перешли на страницу регистрации",
            )
            logging.info(f"URL после клика: {selenium.current_url}")
            assert account_page.is_register_form_visible(), (
                "Форма регистрации не отображается"
            )

    @allure.story("Регистрация")
    @allure.title("Регистрация нового пользователя")
    def test_register_new_user(self, selenium):
        import time
        from module.src.Pizzeria.pages.account_page import AccountPage

        # Генерируем уникальные данные каждый запуск.
        # ВАЖНО: не более 20 символов на поле.
        suffix = int(time.time()) % 100000  # 5 цифр: 00000-99999
        username = f"test{suffix}"  # 9 символов
        email = f"t{suffix}@a.ru"  # 11 символов
        password = "qwertyqwer"  # 10 символов

        logging.info(
            f"Регистрируем: username='{username}' ({len(username)} симв.), "
            f"email='{email}' ({len(email)} симв.)"
        )

        account_page = AccountPage(selenium)

        with allure.step("Открываем форму регистрации"):
            account_page.open_register()

        with allure.step("Проверяем, что форма регистрации отображается"):
            assert account_page.is_register_form_visible(), (
                "Форма регистрации не отображается"
            )

        with allure.step(f"Заполняем форму: логин={username}, email={email}"):
            account_page.register(
                username=username, email=email, password=password
            )

        with allure.step("Проверяем, что регистрация прошла успешно"):
            # После регистрации WooCommerce остаётся на /register/ и показывает
            # сообщение "Регистрация завершена"
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 10).until(
                lambda d: account_page.is_registration_successful(),
                message="Нет сообщения об успешной регистрации",
            )
            logging.info(f"URL после регистрации: {selenium.current_url}")
            logging.info("Регистрация успешно завершена")

    @allure.story("Регистрация")
    @allure.title("Проверка авторизации после регистрации")
    def test_login_after_registration(self, selenium, existing_user):
        from module.src.Pizzeria.pages.account_page import AccountPage

        account_page = AccountPage(selenium)

        with allure.step("Открываем страницу «Мой аккаунт»"):
            account_page.open_account()

        with allure.step(
                f"Входим как {existing_user['username']}"
        ):
            account_page.login(
                username=existing_user["username"],
                password=existing_user["password"],
            )

        with allure.step("Проверяем, что пользователь авторизован"):
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 10).until(
                lambda d: account_page.is_logged_in(),
                message="Пользователь не авторизовался",
            )
            logging.info(f"URL: {selenium.current_url}")
            logging.info("Пользователь успешно авторизован")

    @allure.story("Оформление заказа")
    @allure.title("Переход авторизованного к оформлению заказа")
    def test_checkout_authorized(self, checkout_page_ready, selenium):
        with allure.step("Проверяем, что открыта форма оформления"):
            logging.info(f"URL: {selenium.current_url}")
            assert "/checkout/" in selenium.current_url, (
                f"Открылась не форма оформления: {selenium.current_url}"
            )

        with allure.step("Проверяем, что нет требования авторизации"):
            assert not checkout_page_ready.is_login_required(), (
                "Форма требует авторизации, хотя мы залогинены"
            )

    @allure.story("Оформление заказа")
    @allure.title("Заполнение данных доставки")
    def test_fill_delivery_data(self, checkout_page_ready):
        with allure.step("Заполняем данные доставки"):
            checkout_page_ready.fill_delivery_data(
                first_name="Олег",
                last_name="Олегович",
                address="Пушкина 44",
                city="Москва",
                state="Московская",
                postcode="101000",
                phone="+79991234567",
                order_date="2026-10-06",
                comments="Тестовый заказ",
            )

        with allure.step("Проверяем, что поля заполнены"):
            from module.src.Pizzeria.locators.checkout_page_locators import (
                CheckoutPageLocators,
            )
            first_name = checkout_page_ready.find_element(
                CheckoutPageLocators.FIRST_NAME
            ).get_attribute("value")
            assert first_name == "Олег", (
                f"Имя не заполнено: '{first_name}'"
            )

    @allure.story("Оформление заказа")
    @allure.title("Выбор способа оплаты «При доставке»")
    def test_select_payment(self, checkout_page_ready):
        with allure.step("Заполняем данные доставки"):
            checkout_page_ready.fill_delivery_data(
                first_name="Олег",
                last_name="Олегович",
                address="Пушкина 44",
                city="Москва",
                state="Московская",
                postcode="101000",
                phone="+79991234567",
                order_date="2026-10-06",
            )

        with allure.step("Выбираем оплату «При доставке»"):
            checkout_page_ready.select_payment_cod()

        with allure.step("Проверяем, что оплата выбрана"):
            from module.src.Pizzeria.locators.checkout_page_locators import (
                CheckoutPageLocators,
            )
            radio = checkout_page_ready.find_element(
                CheckoutPageLocators.PAYMENT_COD
            )
            assert radio.is_selected(), "Оплата «При доставке» не выбрана"

    @allure.story("Оформление заказа")
    @allure.title("Подтверждение заказа")
    def test_confirm_order(self, checkout_page_ready, selenium):
        with allure.step("Заполняем данные доставки"):
            checkout_page_ready.fill_delivery_data(
                first_name="Олег",
                last_name="Олегович",
                address="Пушкина 44",
                city="Москва",
                state="Московская",
                postcode="101000",
                phone="+79991234567",
                order_date="2026-10-06",
            )

        with allure.step("Выбираем оплату «При доставке»"):
            checkout_page_ready.select_payment_cod()

        with allure.step("Принимаем условия"):
            checkout_page_ready.accept_terms()

        with allure.step("Подтверждаем заказ"):
            checkout_page_ready.place_order()

        with allure.step("Проверяем, что заказ оформлен"):
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 15).until(
                lambda d: checkout_page_ready.is_order_received(),
                message="Заказ не подтверждён",
            )
            logging.info("Заказ успешно оформлен")

    @allure.story("Оформление заказа")
    @allure.title("Проверка данных оформленного заказа")
    def test_check_order_in_account(self, checkout_page_ready, selenium):
        with allure.step("Заполняем данные доставки"):
            checkout_page_ready.fill_delivery_data(
                first_name="Олег",
                last_name="Олегович",
                address="Пушкина 44",
                city="Москва",
                state="Московская",
                postcode="101000",
                phone="+79991234567",
                order_date="2026-10-06",
            )

        with allure.step("Выбираем оплату и подтверждаем заказ"):
            checkout_page_ready.select_payment_cod()
            checkout_page_ready.accept_terms()
            checkout_page_ready.place_order()

        with allure.step("Ждём подтверждения заказа"):
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(selenium, 15).until(
                lambda d: checkout_page_ready.is_order_received(),
                message="Заказ не подтверждён",
            )

        with allure.step("Переходим в «Мой аккаунт» → Заказы"):
            selenium.get("https://pizzeria.skillbox.cc/my-account/orders/")

        with allure.step("Проверяем, что в списке есть заказ"):
            from selenium.webdriver.common.by import By
            orders = selenium.find_elements(By.CSS_SELECTOR, ".woocommerce-orders-table__row")
            logging.info(f"Заказов в аккаунте: {len(orders)}")
            assert len(orders) > 0, "В личном кабинете нет заказов"

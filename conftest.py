import logging.config
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


project_root = Path(__file__).resolve().parent
log_file_path = project_root / 'logging.ini'
logging.config.fileConfig(log_file_path)


@pytest.fixture
def selenium():
    options = Options()
    options.set_capability("browserVersion", "latest")
    options.set_capability("platformName", "windows")
    logging.info(f"options: {options}")

    service = Service(ChromeDriverManager().install())
    selenium = webdriver.Chrome(service=service, options=options)

    # Сначала открываем сайт — иначе localStorage/sessionStorage недоступны
    selenium.get("https://pizzeria.skillbox.cc/")

    # Очищаем cookies и localStorage, чтобы каждый тест начинал с чистой сессии
    selenium.delete_all_cookies()
    selenium.execute_script("window.localStorage.clear();")
    selenium.execute_script("window.sessionStorage.clear();")

    logging.info(f"selenium: {selenium}")

    yield selenium

    selenium.quit()
    logging.info("Браузер успешно закрыт")

@pytest.fixture
def existing_user():
    """Заранее созданный пользователь для тестов логина и оформления заказа."""
    return {
        "username": "test777test",
        "password": "qwertyqwer",
        "email": "test777test@mail.ru",
    }

@pytest.fixture
def checkout_page_ready(selenium, existing_user):
    """Логин + товар в корзине + открытая форма оформления."""
    from module.src.Pizzeria.pages.main_page import MainPage
    from module.src.Pizzeria.pages.account_page import AccountPage
    from module.src.Pizzeria.pages.cart_page import CartPage
    from module.src.Pizzeria.pages.checkout_page import CheckoutPage

    # Логин
    account_page = AccountPage(selenium)
    account_page.open_account()
    account_page.login(
        username=existing_user["username"],
        password=existing_user["password"],
    )

    # Очищаем корзину через цикл удаления
    main_page = MainPage(selenium)
    main_page.open()
    main_page.go_to_cart()
    cart_page = CartPage(selenium)

    logging.info(f"Позиций в корзине до очистки: {cart_page.get_items_count()}")
    while cart_page.get_items_count() > 0:
        cart_page.remove_item(index=0)
    logging.info("Корзина очищена")

    # Добавляем ровно одну пиццу
    main_page.open()
    main_page.add_pizza_and_wait(index=0)

    # Переходим к оформлению
    main_page.go_to_cart()
    cart_page.go_to_checkout()

    yield CheckoutPage(selenium)
from selenium.webdriver.common.by import By


class MainPageLocators:
    # --- Навигация ---
    MENU_LINK = (By.CSS_SELECTOR, "#menu-item-389 > a")
    CART_LINK = (By.LINK_TEXT, "Корзина")
    ACCOUNT_LINK = (By.LINK_TEXT, "Мой аккаунт")
    BONUS_LINK = (By.LINK_TEXT, "Бонусная программа")
    CHECKOUT_LINK = (By.LINK_TEXT, "Оформление заказа")

    # --- Слайдер с пиццами (внутри #product1) ---
    PIZZA_SLIDER = (By.CSS_SELECTOR, "#product1 .slick-slider")
    PIZZA_SLIDE = (By.CSS_SELECTOR, "#product1 li.slick-slide")
    PIZZA_SLIDE_ACTIVE = (By.CSS_SELECTOR, "#product1 li.slick-slide.slick-active")
    PIZZA_IMAGE_ACTIVE = (
        By.CSS_SELECTOR,
        "#product1 li.slick-slide.slick-active .item-img a img",
    )
    ADD_TO_CART_BUTTON_ACTIVE = (
        By.CSS_SELECTOR,
        "#product1 li.slick-slide.slick-active a.add_to_cart_button",
    )
    SLIDER_NEXT = (By.CSS_SELECTOR, "#product1 .slick-next")
    SLIDER_PREV = (By.CSS_SELECTOR, "#product1 .slick-prev")
    SLICK_TRACK = (By.CSS_SELECTOR, "#product1 .slick-track")

    # --- Секции ---
    SECTION_PIZZA_TITLE = (By.XPATH, "//*[contains(text(), 'ПИЦЦА')]")
    SECTION_DESSERT_TITLE = (By.XPATH, "//*[contains(text(), 'ДЕСЕРТЫ')]")

    # --- Корзина в шапке ---
    CART_CONTENTS = (By.CSS_SELECTOR, "a.cart-contents")

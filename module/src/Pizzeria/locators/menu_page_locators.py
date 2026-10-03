from selenium.webdriver.common.by import By


class MenuPageLocators:
    # Список товаров
    PRODUCTS_LIST = (By.CSS_SELECTOR, "ul.products")
    PRODUCT_ITEM = (By.CSS_SELECTOR, "ul.products li.product")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "ul.products li.product h3")
    PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        "ul.products li.product .price .woocommerce-Price-amount",
    )
    PRODUCT_ADD_TO_CART = (
        By.CSS_SELECTOR,
        "ul.products li.product a.add_to_cart_button",
    )

    # Заголовок страницы
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.entry-title")

    # Фильтр по цене
    PRICE_FILTER_FORM = (By.CSS_SELECTOR, "#woocommerce_price_filter-2 form")
    MIN_PRICE = (By.ID, "min_price")
    MAX_PRICE = (By.ID, "max_price")
    APPLY_FILTER_BUTTON = (
        By.CSS_SELECTOR,
        "#woocommerce_price_filter-2 button[type='submit']",
    )

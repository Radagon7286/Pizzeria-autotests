from selenium.webdriver.common.by import By


class ProductPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "p.price .woocommerce-Price-amount")
    BOARD_PACK_SELECT = (By.ID, "board_pack")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.single_add_to_cart_button")
    BREADCRUMB = (By.CSS_SELECTOR, ".woocommerce-breadcrumb")

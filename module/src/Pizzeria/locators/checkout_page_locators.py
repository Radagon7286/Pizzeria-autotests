from selenium.webdriver.common.by import By


class CheckoutPageLocators:
    # Заголовок
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.post-title")

    # Сообщение о необходимости логина
    LOGIN_REQUIRED_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-info")
    LOGIN_LINK = (By.CSS_SELECTOR, "a.showlogin")

    # Поля доставки
    FIRST_NAME = (By.ID, "billing_first_name")
    LAST_NAME = (By.ID, "billing_last_name")
    COUNTRY = (By.ID, "billing_country")
    ADDRESS = (By.ID, "billing_address_1")
    CITY = (By.ID, "billing_city")
    STATE = (By.ID, "billing_state")
    POSTCODE = (By.ID, "billing_postcode")
    PHONE = (By.ID, "billing_phone")
    EMAIL = (By.ID, "billing_email")
    ORDER_DATE = (By.ID, "order_date")
    ORDER_COMMENTS = (By.ID, "order_comments")

    # Оплата
    PAYMENT_BACS = (By.ID, "payment_method_bacs")
    PAYMENT_COD = (By.ID, "payment_method_cod")

    # Согласие с условиями
    TERMS_CHECKBOX = (By.ID, "terms")

    # Кнопка подтверждения
    PLACE_ORDER_BUTTON = (By.ID, "place_order")

    # Сообщение об успешном заказе
    ORDER_RECEIVED = (By.CSS_SELECTOR, ".woocommerce-order")

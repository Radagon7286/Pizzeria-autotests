from selenium.webdriver.common.by import By


class CartPageLocators:
    # Строки товаров
    CART_ITEM = (By.CSS_SELECTOR, "tr.woocommerce-cart-form__cart-item")
    ITEM_NAME = (By.CSS_SELECTOR, "td.product-name a")
    ITEM_PRICE = (By.CSS_SELECTOR, "td.product-price")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "td.product-quantity input.qty")
    ITEM_SUBTOTAL = (By.CSS_SELECTOR, "td.product-subtotal")
    ITEM_REMOVE = (By.CSS_SELECTOR, "td.product-remove a.remove")

    # Обновление корзины
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, "button[name='update_cart']")

    # Кнопка "Перейти к оплате"
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a.checkout-button")

    # Строка купона в "Общей сводке"
    COUPON_AMOUNT = (By.CSS_SELECTOR, ".cart-discount .amount")

    # Купон
    COUPON_INPUT = (By.ID, "coupon_code")
    APPLY_COUPON_BUTTON = (By.CSS_SELECTOR, "button[name='apply_coupon']")
    COUPON_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-message")
    COUPON_ERROR_MESSAGE = (By.CSS_SELECTOR, ".woocommerce-error")

    # Строка купона
    COUPON_ROW = (By.CSS_SELECTOR, "tr.cart-discount")

    # Кнопка "Удалить" купон
    REMOVE_COUPON = (By.CSS_SELECTOR, "a.woocommerce-remove-coupon")

    # Итоговая сумма
    CART_TOTAL = (By.CSS_SELECTOR, ".cart_totals .order-total .amount")

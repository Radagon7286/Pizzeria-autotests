from selenium.webdriver.common.by import By


class AccountPageLocators:
    # Заголовок страницы
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.post-title")

    # Форма логина (на /my-account/)
    LOGIN_FORM = (By.CSS_SELECTOR, "form.woocommerce-form-login")
    LOGIN_USERNAME = (By.ID, "username")
    LOGIN_PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[name='login']")

    # Кнопка "Зарегистрироваться" (редиректит на /register/)
    REGISTER_LINK_BUTTON = (By.CSS_SELECTOR, "button.custom-register-button")

    # Форма регистрации (на /register/)
    REGISTER_FORM = (By.CSS_SELECTOR, "form.woocommerce-form-register")
    REGISTER_USERNAME = (By.ID, "reg_username")
    REGISTER_EMAIL = (By.ID, "reg_email")
    REGISTER_PASSWORD = (By.ID, "reg_password")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[name='register']")
    REGISTER_SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'content-page')]//div[contains(text(), 'Регистрация завершена')]"
    )

    # Признак успешного входа (после логина)
    LOGOUT_LINK = (By.LINK_TEXT, "Выйти")
    ACCOUNT_CONTENT = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")

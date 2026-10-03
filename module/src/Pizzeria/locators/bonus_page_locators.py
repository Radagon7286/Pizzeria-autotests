from selenium.webdriver.common.by import By


class BonusPageLocators:
    # Форма
    NAME_INPUT = (By.ID, "bonus_username")
    PHONE_INPUT = (By.ID, "bonus_phone")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[name='bonus']")

    # Контейнер с сообщениями (ошибки и успех)
    MESSAGE_CONTAINER = (By.ID, "bonus_content")
    MAIN_CONTAINER = (By.ID, "bonus_main")

    # Признаки успеха
    SUCCESS_TEXT = "Ваша карта оформлена!"

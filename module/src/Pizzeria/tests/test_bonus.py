import logging

import allure

from module.src.Pizzeria.pages.bonus_page import BonusPage


@allure.feature("Бонусная программа")
class TestBonus:

    @allure.story("Основной сценарий")
    @allure.title("Оформление карты с валидными данными")
    def test_bonus_valid(self, selenium):
        page = BonusPage(selenium)

        with allure.step("Открываем страницу бонусной программы"):
            page.open()

        with allure.step("Заполняем форму: имя + телефон"):
            page.fill_form(name="Тест", phone="+78000000000")

        with allure.step("Нажимаем «Оформить карту»"):
            page.submit()

        with allure.step("Закрываем alert, если появился"):
            from selenium.common.exceptions import NoAlertPresentException
            try:
                selenium.switch_to.alert.accept()
                logging.info("Alert закрыт")
            except NoAlertPresentException:
                logging.info("Alert не появился")

        with allure.step("Ждём появления сообщения об успехе"):
            assert page.is_card_created(timeout=15), (
                "Карта не оформлена — сообщение не появилось"
            )
            logging.info("Карта оформлена")

    @allure.story("Валидация")
    @allure.title("Ошибка при пустом поле «Имя»")
    def test_bonus_empty_name(self, selenium):
        page = BonusPage(selenium)
        page.open()

        with allure.step("Оставляем имя пустым, телефон заполняем"):
            page.fill_form(name="", phone="+78000000000")

        with allure.step("Нажимаем «Оформить карту»"):
            page.submit()

        with allure.step("Проверяем ошибку"):
            error = page.get_error_message()
            logging.info(f"Ошибка: '{error}'")
            assert "Имя" in error and "обязательно" in error, (
                f"Ожидалась ошибка про имя, получено: '{error}'"
            )

    @allure.story("Валидация")
    @allure.title("Ошибка при пустом поле «Телефон»")
    def test_bonus_empty_phone(self, selenium):
        page = BonusPage(selenium)
        page.open()

        with allure.step("Имя заполняем, телефон пустой"):
            page.fill_form(name="Тест", phone="")

        with allure.step("Нажимаем «Оформить карту»"):
            page.submit()

        with allure.step("Проверяем ошибку"):
            error = page.get_error_message()
            logging.info(f"Ошибка: '{error}'")
            assert "Телефон" in error and "обязательно" in error, (
                f"Ожидалась ошибка про телефон, получено: '{error}'"
            )

    @allure.story("Валидация")
    @allure.title("Ошибка при неверном формате телефона")
    def test_bonus_invalid_phone(self, selenium):
        page = BonusPage(selenium)
        page.open()

        with allure.step("Заполняем телефон неверного формата"):
            page.fill_form(name="Тест", phone="123")

        with allure.step("Нажимаем «Оформить карту»"):
            page.submit()

        with allure.step("Проверяем ошибку формата"):
            error = page.get_error_message()
            logging.info(f"Ошибка: '{error}'")
            assert "неверный формат" in error.lower(), (
                f"Ожидалась ошибка формата, получено: '{error}'"
            )

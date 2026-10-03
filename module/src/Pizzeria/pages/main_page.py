import logging
import re

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from module.src.Pizzeria.base_page import BasePage
from module.src.Pizzeria.locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, base_url="https://pizzeria.skillbox.cc/")

    @allure.step("Перейти в раздел 'Меню'")
    def go_to_menu(self):
        logging.info("Переходим в Меню")
        element = self.find_element(MainPageLocators.MENU_LINK)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Перейти в 'Корзину'")
    def go_to_cart(self):
        logging.info("Переходим в Корзину")
        self.click(MainPageLocators.CART_LINK)

    @allure.step("Перейти в 'Мой аккаунт'")
    def go_to_account(self):
        logging.info("Переходим в Мой аккаунт")
        self.click(MainPageLocators.ACCOUNT_LINK)

    @allure.step("Перейти в 'Бонусную программу'")
    def go_to_bonus(self):
        logging.info("Переходим в Бонусную программу")
        self.click(MainPageLocators.BONUS_LINK)

    @allure.step("Навести курсор на пиццу #{index} в слайдере")
    def hover_pizza(self, index=0):
        """Навести мышь на картинку пиццы внутри конкретного слайда."""
        slides = self.find_elements(MainPageLocators.PIZZA_SLIDE_ACTIVE)
        logging.info(f"Наводим на картинку пиццы в слайде #{index}")
        image = slides[index].find_element(By.CSS_SELECTOR, ".item-img a img")
        self.actions.move_to_element(image).pause(0.5).perform()

    @allure.step("Добавить пиццу #{index} из слайдера в корзину")
    def add_pizza_to_cart(self, index=0):
        """Навести мышь на пиццу и кликнуть 'В корзину' в этом же слайде."""
        slides = self.find_elements(MainPageLocators.PIZZA_SLIDE_ACTIVE)
        slide = slides[index]

        # 1. Наводим мышь на картинку внутри этого слайда
        image = slide.find_element(By.CSS_SELECTOR, ".item-img a img")
        logging.info(f"Наводим на картинку пиццы в слайде #{index}")
        self.actions.move_to_element(image).pause(0.5).perform()

        # 2. Кликаем по кнопке внутри этого же слайда
        button = slide.find_element(By.CSS_SELECTOR, "a.add_to_cart_button")
        logging.info(f"Кликаем 'В корзину' в слайде #{index}")
        self.actions.move_to_element(button).click().perform()

    @allure.step("Добавить пиццу #{index} и дождаться обновления корзины")
    def add_pizza_and_wait(self, index=0):
        """Добавить пиццу и дождаться, пока счётчик корзины обновится."""
        total_before = self.get_cart_total()
        self.add_pizza_to_cart(index=index)
        self.wait_cart_total_changed(total_before)
        logging.info("Товар добавлен, счётчик корзины обновился")

    @allure.step("Переключить слайдер вперёд")
    def click_slider_next(self):
        logging.info("Листаем слайдер вперёд")
        self.hover_slider()
        self.click(MainPageLocators.SLIDER_NEXT)

    @allure.step("Переключить слайдер назад")
    def click_slider_prev(self):
        logging.info("Листаем слайдер назад")
        self.hover_slider()
        self.click(MainPageLocators.SLIDER_PREV)

    @allure.step("Навести мышь на слайдер")
    def hover_slider(self):
        slider = self.find_element(MainPageLocators.PIZZA_SLIDER)
        self.actions.move_to_element(slider).pause(0.5).perform()

    @allure.step("Получить количество слайдов в слайдере")
    def get_slides_count(self):
        """Вернуть количество слайдов в слайдере."""
        slides = self.find_elements(MainPageLocators.PIZZA_SLIDE)
        logging.info(f"Найдено слайдов: {len(slides)}")
        return len(slides)

    @allure.step("Проверить, что слайдер отображается")
    def is_slider_displayed(self):
        """Проверить, что слайдер отображается."""
        slider = self.find_element(MainPageLocators.PIZZA_SLIDER)
        logging.info(f"Слайдер найден: {slider.is_displayed()}")
        return slider.is_displayed()

    @allure.step("Получить текущий сдвиг слайдера")
    def get_slider_offset(self):
        """Вернуть X-смещение слайдера пицц."""
        style = self.find_element(MainPageLocators.SLICK_TRACK).get_attribute("style")
        logging.info(f"Style слайдера: {style}")

        if not style:
            return None

        match = re.search(r"translate3d\((-?\d+(?:\.\d+)?)px", style)
        return float(match.group(1)) if match else None

    @allure.step("Получить opacity кнопки 'В корзину' в слайде #{index}")
    def get_button_opacity(self, index=0):
        """Вернуть CSS-свойство opacity кнопки 'В корзину' в слайде."""
        slides = self.find_elements(MainPageLocators.PIZZA_SLIDE_ACTIVE)
        slide = slides[index]
        button = slide.find_element(By.CSS_SELECTOR, "a.add_to_cart_button")
        opacity = button.value_of_css_property("opacity")
        logging.info(f"Opacity кнопки в слайде #{index}: {opacity}")
        return opacity

    @allure.step("Получить текст счётчика корзины")
    def get_cart_total(self):
        """Вернуть текст счётчика корзины из шапки сайта."""
        total = self.get_text(MainPageLocators.CART_CONTENTS)
        logging.info(f"Текст корзины: {total}")
        return total

    @allure.step("Ожидать, пока текст корзины изменится")
    def wait_cart_total_changed(self, previous_total, timeout=15):
        """Ждать, пока счётчик корзины в шапке изменится."""
        from selenium.common.exceptions import (
            NoSuchElementException,
            StaleElementReferenceException,
        )

        logging.info(f"Ждём изменения корзины (текущее: '{previous_total}')")

        def _check(driver):
            try:
                text = driver.find_element(
                    *MainPageLocators.CART_CONTENTS
                ).text
                return text != previous_total
            except (NoSuchElementException, StaleElementReferenceException):
                return False

        WebDriverWait(self.driver, timeout).until(
            _check,
            message=f"Корзина не обновилась за {timeout} секунд",
        )
        new_total = self.get_text(MainPageLocators.CART_CONTENTS)
        logging.info(f"Новый текст корзины: '{new_total}'")
        return new_total

    @allure.step("Кликнуть по картинке пиццы в слайде #{index}")
    def click_pizza_image(self, index=0):
        """Кликнуть по картинке пиццы в активном слайде."""
        slides = self.find_elements(MainPageLocators.PIZZA_SLIDE_ACTIVE)
        image = slides[index].find_element(By.CSS_SELECTOR, ".item-img a img")
        logging.info(f"Кликаем по картинке пиццы в слайде #{index}")
        image.click()

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


@allure.feature('Full Account')
@allure.story('Waiting page load')
class TestCases:

    @allure.title('Поиск задач со словом "bug"')
    def test_1(self, selenium):
        with allure.step('Открываем страницу issues VS Code'):
            selenium.get('https://github.com/microsoft/vscode/issues')

        with allure.step('Находим поле поиска'):
            el_input = selenium.find_element(
                By.CSS_SELECTOR, "input[name='repository-inputname'"
            )

        with allure.step('Вводим запрос "in:title bug" и нажимаем Enter'):
            el_input.send_keys("in:title bug")
            el_input.send_keys(Keys.ENTER)

        with allure.step('Ожидаем загрузку результатов'):
            time.sleep(5)

    @allure.title('Поиск элемента "bpasero" с помощью дропдауна')
    def test_2(self, selenium):
        with allure.step('Открываем страницу issues VS Code'):
            selenium.get('https://github.com/microsoft/vscode/issues')

        with allure.step('Кликаем по кнопке «Author»'):
            el_button = WebDriverWait(selenium, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[aria-label='Filter by author']")
                )
            )
            el_button.click()

        with allure.step('Ждём появления поля ввода «Filter authors»'):
            el_input = WebDriverWait(selenium, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Filter authors']")
                )
            )

        with allure.step('Вводим "bpasero" через ActionChains'):
            actions = ActionChains(selenium)
            actions.move_to_element(el_input).click().send_keys("bpasero").perform()
            time.sleep(2)

        with allure.step('Ожидаем появления выпадающего списка'):
            time.sleep(5)

        with allure.step('Кликаем по опции "author:bpasero"'):
            el_options = selenium.find_element(
                By.XPATH,
                "//li[@role='option'][.//span[contains(text(), 'author:bpasero')]]"
            )
            el_options.click()

        with allure.step('Проверяем результат'):
            time.sleep(5)

    @allure.title('Поиск репозитория по заданным критериям')
    def test_3(self, selenium):
        with allure.step('Открываем страницу расширенного поиска GitHub'):
            selenium.get('https://github.com/search/advanced')

        with allure.step('Выбираем язык Python в дропдауне'):
            python_option = selenium.find_element(
                By.XPATH, "//select[@id='search_language']//option[@value='Python']"
            )
            python_option.click()

        with allure.step('Вводим количество звёзд ">2000"'):
            el_stars = selenium.find_element(By.XPATH, '//input[@id="search_stars"]')
            el_stars.click()
            el_stars.send_keys(">2000")
            time.sleep(5)

        with allure.step('Вводим имя файла "environment.yml"'):
            el_file_name = selenium.find_element(
                By.XPATH, '//input[@id="search_filename"]'
            )
            el_file_name.click()
            el_file_name.send_keys("environment.yml")
            time.sleep(5)

        with allure.step('Скроллим к кнопке поиска и кликаем'):
            el_button = selenium.find_element(
                By.XPATH, '//button[@class="btn flex-auto"]'
            )
            selenium.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", el_button
            )
            time.sleep(1)
            el_button.click()

        with allure.step('Проверяем результат'):
            time.sleep(5)

    @allure.title('Фильтрация профессий с помощью фильтров')
    def test_4(self, selenium):
        with allure.step('Разворачиваем браузер на полный экран'):
            selenium.set_window_size(1920, 1080)
            time.sleep(2)

        with allure.step('Открываем страницу профессий Skillbox'):
            selenium.get('https://skillbox.ru/code/?type=profession')
            time.sleep(5)

        with allure.step('Фильтр «Длительность» → «От 6 до 12 мес.»'):
            el_dropdawn2 = selenium.find_element(
                By.XPATH,
                "//button[contains(@class, 'ui-round-select__field') "
                "and contains(., 'Длительность')]"
            )
            el_dropdawn2.click()
            el_definite = selenium.find_element(
                By.XPATH, '//ul/li[text()="От 6 до 12 мес."]'
            )
            el_definite.click()
            time.sleep(1)

        with allure.step('Фильтр «Тематика» → открываем дропдаун'):
            el_button2 = selenium.find_element(
                By.XPATH,
                "//button[contains(@class, 'ui-round-select__field') "
                "and contains(., 'Тематика')]"
            )
            time.sleep(1)
            el_button2.click()
            time.sleep(2)

        with allure.step('Выбираем значение «1С» в списке'):
            el_option = selenium.find_element(
                By.XPATH,
                "//li[contains(@class, 'ui-round-select__item') "
                "and contains(., '1С')]"
            )
            el_option.click()

        with allure.step('Нажимаем кнопку «Применить»'):
            el_button3 = selenium.find_element(
                By.XPATH, "//button[contains(., 'Применить')]"
            )
            el_button3.click()

        with allure.step('Проверяем результат'):
            time.sleep(5)

    @allure.title('Наведение мышки на график')
    def test_5(self, selenium):
        with allure.step('Открываем страницу графика коммитов'):
            selenium.get('https://github.com/microsoft/vscode/graphs/commit-activity')
            time.sleep(5)

        with allure.step('Находим столбики графика'):
            bars = selenium.find_elements(
                By.CSS_SELECTOR, ".highcharts-column-series path"
            )
            bar = bars[5]

        with allure.step('Наводим мышку на выбранный столбик'):
            ActionChains(selenium).move_to_element(bar).perform()

        with allure.step('Проверяем результат'):
            time.sleep(5)

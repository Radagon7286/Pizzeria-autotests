from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class TestCases:
    def test_1(self, set_up_browser):
        driver = set_up_browser
        driver.get('https://github.com/microsoft/vscode/issues') # открыть сайт

        el_input = driver.find_element(By.CSS_SELECTOR, "input[name='repository-inputname'") # найти input

        el_input.send_keys("in:title bug") # ввести значение
        el_input.send_keys(Keys.ENTER) # нажать enter

        time.sleep(5)

    def test_2(self, set_up_browser):
        driver = set_up_browser
        driver.get('https://github.com/microsoft/vscode/issues')

        # 1. Ждём и кликаем кнопку Author
        el_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Filter by author']"))
        )
        el_button.click()

        # 2. Ждём инпут
        el_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Filter authors']"))
        )

        # 3. Вводим текст через ActionChains
        actions = ActionChains(driver)
        actions.move_to_element(el_input).click().send_keys("bpasero").perform()
        time.sleep(2)

        # 4. Проверяем, что текст введён
        time.sleep(5)

        # 5. Найти и кликнуть
        el_opions = driver.find_element(By.XPATH, "//li[@role='option']\
            [.//span[contains(text(), 'author:bpasero')]]")
        el_opions.click()

        # 6. Проверяем, что все правильно
        time.sleep(5)


    def test_3(self, set_up_browser):
        driver = set_up_browser
        driver.get('https://github.com/search/advanced')

        # 1. находим в дропдауне элемент и кликаем

        python_option = driver.find_element(
            By.XPATH, "//select[@id='search_language']//option[@value='Python']"
        )
        python_option.click()

        # 2. находим интпут и вводим значение

        el_stars = driver.find_element(By.XPATH, '//input[@id="search_stars"]')
        el_stars.click()
        el_stars.send_keys(">2000")

        time.sleep(5)

        # 3. находим интпут и вводим значение

        el_file_name = driver.find_element(By.XPATH, '//input[@id="search_filename"]')
        el_file_name.click()
        el_file_name.send_keys("environment.yml")

        time.sleep(5)

        # 4. находим и нажимаем на кнопку поиска

        el_button = driver.find_element(By.XPATH, '//button[@class="btn flex-auto"]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el_button)
        time.sleep(1)
        el_button.click()

        # 5. Проверяем, что все правильно

        time.sleep(5)


    def test_4(self, set_up_browser):
        driver = set_up_browser

        # Развернуть в полный экран

        driver.set_window_size(1920, 1080)
        time.sleep(2)

        driver.get('https://skillbox.ru/code/?type=profession')

        time.sleep(5)

        # 1. находим фильтр длительность и выбираем значение

        el_dropdawn2 = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'ui-round-select__field') and contains(., 'Длительность')]"
        )
        el_dropdawn2.click()
        el_definite = driver.find_element(By.XPATH, ('//ul/li[text()="От 6 до 12 мес."]'))
        el_definite.click()

        time.sleep(1)

        # 2. находим фильтр тематика и выбираем значение

        el_button2 = driver.find_element(By.XPATH, "//button[contains(@class, 'ui-round-select__field') and contains\
         (., 'Тематика')]")
        time.sleep(1)
        el_button2.click()
        time.sleep(2)

        # 3. Находим и кликаем на значение

        el_option = driver.find_element(
            By.XPATH, "//li[contains(@class, 'ui-round-select__item') and contains(., '1С')]"
        )
        el_option.click()

        # 4. Нажимаем на кнопку "применить"

        el_button3 = driver.find_element(By.XPATH, "//button[contains(., 'Применить')]")
        el_button3.click()

        # 5. Проверяем, что все правильно

        time.sleep(5)


    def test_5(self, set_up_browser):
        driver = set_up_browser
        driver.get('https://github.com/microsoft/vscode/graphs/commit-activity')
        time.sleep(5)

        # 1. Находим элемент

        bars = driver.find_elements(By.CSS_SELECTOR, ".highcharts-column-series path")
        bar = bars[5]

        # 2. Наводим на элемент

        ActionChains(driver).move_to_element(bar).perform()

        # 3. Проверяем

        time.sleep(5)







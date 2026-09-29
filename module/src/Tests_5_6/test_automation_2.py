import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

@allure.feature('Full Account')
@allure.story('Waiting page load')
class TestCases2:
    @allure.title('Поиск задач со словом "bug"')
    def test_1(self, selenium):
        wait = WebDriverWait(selenium, 15)

        with allure.step('Открываем страницу'):
            selenium.get("https://github.com/microsoft/vscode/issues")

        with allure.step('Вводим поисковый запрос в поле поиска'):
            search_input = wait.until(EC.presence_of_element_located(
                (By.ID, "repository-input")
            ))
            search_input.click()
            search_input.send_keys("in:title bug")
            search_input.send_keys(Keys.ENTER)

        with allure.step('Ждём появления заголовков задач'):
            title_locator = (
                By.CSS_SELECTOR,
                'a[href*="/microsoft/vscode/issues/"]'
            )
            wait.until(EC.presence_of_all_elements_located(title_locator))

        with allure.step('Собираем тексты заголовков'):
            all_links = selenium.find_elements(*title_locator)
            titles = []
            for el in all_links:
                text = el.text.strip()
                if text and not text.lstrip("#").isdigit():
                    titles.append(text)

        print(f"Найдено задач: {len(titles)}")

        with allure.step('Проверяем, что поиск вернул результаты'):
            assert len(titles) > 0, "Поиск не вернул ни одной задачи"
        print(f"✅ Найдено {len(titles)} задач по запросу 'in:title bug'")

    @allure.title('Поиск элемента "brasero" с помощью дропдауна')
    def test_2(self, selenium):
        wait = WebDriverWait(selenium, 15)
        with allure.step('Открываем страницу'):
            selenium.get('https://github.com/microsoft/vscode/issues')

        with allure.step('Открываем страницу и нажимаем на кнопку "author"'):
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Filter by author']")
            )).click()

        with allure.step('Ввод имени:"brasero"'):
            el_input = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Filter authors']")
            ))
            el_input.send_keys("bpasero")

        with allure.step('Выбор пункта author:"bpasero"'):
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//li[@role='option'][.//*[contains(text(), 'author:bpasero')]]")
            )).click()

        with allure.step('Ждём, что фильтр применился'):
            wait.until(lambda d: "bpasero" in d.current_url)

        with allure.step('Получаем все задачи'):
            wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]')
            ))
            titles = [el.text for el in selenium.find_elements(
                By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]'
            )]
            assert titles, "Список задач пуст — фильтр не сработал?"

        with allure.step('Проверка, что фильтр по автору "bpasero" применился'):
            assert "bpasero" in selenium.current_url, \
                f"В URL нет фильтра по автору: {selenium.current_url}"

    @allure.title('Поиск репозитория по заданым критериям')
    def test_3(self, selenium):
        wait = WebDriverWait(selenium, 15)

        with allure.step('Открываем страницу'):
            selenium.get('https://github.com/search/advanced')

        with allure.step('Выбор языка Python'):
            select_el = wait.until(EC.presence_of_element_located((By.ID, "search_language")))
            Select(select_el).select_by_value("Python")

        with allure.step('Звёзды'):
            el_stars = selenium.find_element(By.ID, "search_stars")
            el_stars.click()
            el_stars.send_keys(">20000")

        with allure.step('Имя файла'):
            el_file_name = selenium.find_element(By.ID, "search_filename")
            el_file_name.click()
            el_file_name.send_keys("environment.yml")

        with allure.step('Кнопка поиска'):
            el_button = selenium.find_element(By.CSS_SELECTOR, "button[type='submit'].btn")
            selenium.execute_script("arguments[0].scrollIntoView({block: 'center'});", el_button)
            el_button.click()

        with allure.step('Ждём загрузки результатов'):
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a[href$="/stargazers"]')
            ))

        with allure.step('Собираем звёзды у каждой карточки'):
            star_links = selenium.find_elements(By.CSS_SELECTOR, 'a[href$="/stargazers"]')
            raw_aria = [a.get_attribute("aria-label") for a in star_links]
        print("Сырые aria-label:", raw_aria)

        assert raw_aria, "Не нашли ни одной ссылки на stargazers — проверь селектор"

        stars = []
        for label in raw_aria:
            m = re.search(r"([\d,]+)\s*star", label or "")
            if m:
                stars.append(int(m.group(1).replace(",", "")))

        print("Распарсенные звёзды:", stars)
        assert stars, "Не удалось распарсить звёзды из aria-label"

        with allure.step('8. Проверка: все звёзды > 20000'):
            bad = [s for s in stars if s <= 20000]
        assert not bad, f"Найдены репозитории со звёздами ≤20000: {bad}"

    @allure.title('Фильтрация профессий с помощью фильтров')
    def test_4(self, selenium):
        wait = WebDriverWait(selenium, 15)

        with allure.step('Открываем страницу по заданному разрешению'):
            selenium.set_window_size(1920, 1080)
            selenium.get('https://skillbox.ru/code/')

        with allure.step('Вкладка «Профессия»'):
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Профессия']")
            )).click()

        with allure.step('Длительность → «От 6 до 12 мес.»'):
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'ui-round-select__field') "
                           "and contains(normalize-space(.), 'Длительность')]")
            )).click()
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(@class, 'ui-round-select__item') "
                           "and normalize-space()='От 6 до 12 мес.']")
            )).click()

        with allure.step('Тематика → первая доступная'):
            # 1. Находим кнопку "Тематика"
            tematika_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[contains(@class, 'ui-round-select__field') "
                 "and contains(normalize-space(.), 'Тематика')]")
            ))

        with allure.step('Скроллим к кнопке «Тематика»'):
            selenium.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", tematika_btn
            )
            time.sleep(0.3)

        with allure.step('Кликаем по кнопке «Тематика» через ActionChains'):
            ActionChains(selenium).move_to_element(tematika_btn).pause(0.2).click().perform()
            print("✅ Кликнули по кнопке 'Тематика'")

        with allure.step('Ждём появления списка опций'):
            options = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR,
                 'ul.ui-round-select__list li.ui-round-select__item')
            ))
            print(f"Найдено опций в списке 'Тематика': {len(options)}")

        with allure.step('Выбираем первую видимую опцию «Тематика»'):
            picked = False
            for opt in options:
                if opt.is_displayed():
                    text = opt.text.strip()
                    print(f"Кликаем по опции: {text!r}")
                    ActionChains(selenium).move_to_element(opt).pause(0.2).click().perform()
                    picked = True
                    break
            assert picked, "Не нашли ни одной видимой опции в списке 'Тематика'"

        with allure.step('Ждём, что фильтр применился (URL содержит duration_min)'):
            wait.until(lambda d: "duration_min" in d.current_url)

        with allure.step('Ждём появления карточек профессий'):
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'li.product-card-new__feature')
            ))

        with allure.step('Собираем длительности из карточек'):
            features = selenium.find_elements(
                By.CSS_SELECTOR, 'li.product-card-new__feature'
            )
            print(f"Найдено feature-элементов: {len(features)}")

            durations_months = []
            for el in features:
                txt = el.text.strip()
                m = re.search(r"(\d+)\s*месяц", txt, re.IGNORECASE)
                if m:
                    durations_months.append(int(m.group(1)))

        with allure.step('Убираем дубликаты и сортируем'):
            durations_months = sorted(set(durations_months))

        print(f"Найденные длительности (мес.): {durations_months}")

        with allure.step('Проверяем, что длительности найдены'):
            assert durations_months, "Не удалось найти длительности на карточках"

        with allure.step('Проверяем, что все длительности в диапазоне 6–12 мес.'):
            bad = [d for d in durations_months if not (6 <= d <= 12)]
            assert not bad, (
                f"Найдены длительности вне диапазона 6–12 мес.: {bad}"
            )

        with allure.step('Финальная проверка пройдена'):
            print(f"✅ Все {len(durations_months)} длительностей "
                  f"в диапазоне 6–12 мес. ✅")

    @allure.title('Проверка тултипа графика коммитов')
    def test_5(self, selenium):
        wait = WebDriverWait(selenium, 15)

        with allure.step('Открываем страницу по заданному разрешению'):
            selenium.set_window_size(1920, 1080)
            selenium.get('https://github.com/microsoft/vscode/graphs/commit-activity')

        with allure.step('Ждём столбики'):
            bars = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".highcharts-column-series path")
            ))
        assert bars, "Не нашли столбики графика"
        print(f"Найдено столбиков: {len(bars)}")

        with allure.step('Берём последний столбик (свежая неделя)'):
            last_index = len(bars) - 1
            bar = bars[last_index]

        with allure.step('Читаем эталон из aria-label столбика'):
            aria_label = bar.get_attribute("aria-label")
        print(f"aria-label столбика: {aria_label!r}")
        assert aria_label, "У столбика нет aria-label"

        m_ref = re.search(r"(\d[\d,]*)\s*[.,]?\s*Commits", aria_label, re.IGNORECASE)
        assert m_ref, f"Не нашли число коммитов в aria-label: {aria_label!r}"
        expected_commits = int(m_ref.group(1).replace(",", ""))
        print(f"Эталонное число коммитов: {expected_commits}")

        with allure.step('Наводим мышку'):
            ActionChains(selenium).move_to_element(bar).perform()

        with allure.step('Ждём тултип'):
            tooltip = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".highcharts-tooltip")
            ))
            tooltip_text = tooltip.text.strip()
        print("Текст тултипа:", repr(tooltip_text))

        with allure.step('Проверяем содержимое'):
            assert "commits" in tooltip_text.lower(), \
                f"В тултипе нет слова 'commits': {tooltip_text!r}"
            assert "week of" in tooltip_text.lower(), \
                f"В тултипе нет 'week of': {tooltip_text!r}"

        with allure.step('Парсим число ИМЕННО после слова "Commits" — так год не попадёт'):
            m = re.search(r"Commits\s+(\d[\d,]*)", tooltip_text, re.IGNORECASE)
        assert m, f"Не нашли число коммитов в тултипе: {tooltip_text!r}"

        actual_commits = int(m.group(1).replace(",", ""))
        print(f"Число из тултипа: {actual_commits}")

        with allure.step('ГЛАВНАЯ ПРОВЕРКА: сравниваем конкретные значения'):
            assert actual_commits == expected_commits, (
                f"Тултип показывает {actual_commits}, "
                f"а в aria-label столбика {expected_commits} — значения не совпадают"
            )

        print("✅ Тултип содержит корректное значение ✅")

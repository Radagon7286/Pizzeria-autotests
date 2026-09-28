from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class TestCases2:
    def test_1(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)

        # 1. Сразу открываем страницу с уже применённым фильтром
        driver.get("https://github.com/microsoft/vscode/issues?q=in%3Atitle+bug")

        # 2.  Ждём появления заголовков
        wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]')
        ))

        titles = [el.text for el in driver.find_elements(
            By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]'
        )]
        print(f"Найдено задач: {len(titles)}")

        assert titles, "Список задач пуст — проверь селектор"

        bad = [t for t in titles if "bug" not in t.lower()]
        assert not bad, (
                f"Найдены задачи без слова 'bug' в названии "
                f"({len(bad)} из {len(titles)}):\n" + "\n".join(bad)
        )


    def test_2(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        driver.get('https://github.com/microsoft/vscode/issues')

        # 1-2. Кнопка Author
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[aria-label='Filter by author']")
        )).click()

        # 3. Ввод имени
        el_input = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Filter authors']")
        ))
        el_input.send_keys("bpasero")

        # 5. Выбор пункта author:bpasero
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@role='option'][.//*[contains(text(), 'author:bpasero')]]")
        )).click()

        # Ждём, что фильтр применился
        wait.until(lambda d: "bpasero" in d.current_url)

        # 6. Получаем все задачи
        wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]')
        ))
        titles = [el.text for el in driver.find_elements(
            By.CSS_SELECTOR, 'a[data-testid="issue-pr-title-link"]'
        )]
        assert titles, "Список задач пуст — фильтр не сработал?"

        # 7. Проверка, что фильтр по автору bpasero применился
        assert "bpasero" in driver.current_url, \
            f"В URL нет фильтра по автору: {driver.current_url}"


    def test_3(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)
        driver.get('https://github.com/search/advanced')

        # 2. Выбор языка Python
        select_el = wait.until(EC.presence_of_element_located((By.ID, "search_language")))
        Select(select_el).select_by_value("Python")

        # 3. Звёзды
        el_stars = driver.find_element(By.ID, "search_stars")
        el_stars.click()
        el_stars.send_keys(">20000")

        # 4. Имя файла
        el_file_name = driver.find_element(By.ID, "search_filename")
        el_file_name.click()
        el_file_name.send_keys("environment.yml")

        # 5. Кнопка поиска
        el_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el_button)
        el_button.click()

        # 6. Ждём загрузки результатов
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[href$="/stargazers"]')
        ))

        # 7. Собираем звёзды у каждой карточки
        star_links = driver.find_elements(By.CSS_SELECTOR, 'a[href$="/stargazers"]')
        raw_aria = [a.get_attribute("aria-label") for a in star_links]
        print("Сырые aria-label:", raw_aria)

        assert raw_aria, "Не нашли ни одной ссылки на stargazers — проверь селектор"

        # Парсим "483996 stars" → 483996
        stars = []
        for label in raw_aria:
            m = re.search(r"([\d,]+)\s*star", label or "")
            if m:
                stars.append(int(m.group(1).replace(",", "")))

        print("Распарсенные звёзды:", stars)
        assert stars, "Не удалось распарсить звёзды из aria-label"

        # 8. Проверка: все звёзды > 20000
        bad = [s for s in stars if s <= 20000]
        assert not bad, f"Найдены репозитории со звёздами ≤20000: {bad}"


    def test_4(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)

        # 1. Открываем страницу
        driver.set_window_size(1920, 1080)
        driver.get('https://skillbox.ru/code/')

        # 2. Вкладка «Профессия»
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Профессия']")
        )).click()

        # 3. Длительность → «От 6 до 12 мес.»
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'ui-round-select__field') "
                       "and contains(normalize-space(.), 'Длительность')]")
        )).click()

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@class, 'ui-round-select__item') "
                       "and normalize-space()='От 6 до 12 мес.']")
        )).click()

        # 4. Тематика → первая доступная
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'ui-round-select__field') "
                       "and contains(normalize-space(.), 'Тематика')]")
        )).click()

        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'ul.ui-round-select__list li.ui-round-select__item')
        )).click()

        # 5. Ждём, что фильтр применился (URL содержит duration_min/duration_max)
        wait.until(lambda d: "duration_min" in d.current_url)

        # 6. Ждём, что карточки с длительностью отрисовались
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[contains(text(), 'трудоустройством')]")
        ))

        # 7. Собираем тексты карточек-родителей
        cards = driver.find_elements(By.CSS_SELECTOR, 'article, [class*="card"]')
        cards_text = [el.text for el in cards if el.text.strip()]
        print("Тексты карточек (первые 3):", cards_text[:3])

        # 8. Парсим длительность из каждой карточки
        durations_months = []
        for txt in cards_text:
            m = re.search(r"(\d+)\s*мес", txt)
            if m:
                durations_months.append(int(m.group(1)))

        # Убираем дубликаты (одна карточка может матчиться на нескольких уровнях)
        durations_months = sorted(set(durations_months))

        print("Найденные длительности (мес.):", durations_months)
        assert durations_months, "Не удалось найти длительности на карточках"

        # 9. Проверка: каждая длительность в диапазоне 6–12
        bad = [d for d in durations_months if not (6 <= d <= 12)]
        assert not bad, f"Карточки с длительностью вне 6–12 мес.: {bad}"

        print("Все длительности в диапазоне 6–12 месяцев ✅")


    def test_5(self, set_up_browser):
        driver = set_up_browser
        wait = WebDriverWait(driver, 15)

        # 1. Открываем график коммитов
        driver.set_window_size(1920, 1080)
        driver.get('https://github.com/microsoft/vscode/graphs/commit-activity')

        # 2. Ждём, что столбики графика отрисовались
        bars = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".highcharts-column-series path")
        ))
        assert bars, "Не нашли столбики графика"
        print(f"Найдено столбиков: {len(bars)}")

        # Берём последний столбик (свежая неделя)
        bar = bars[-1]

        # 3. Наводим мышку на столбик
        ActionChains(driver).move_to_element(bar).perform()

        # 4. Ждём появления тултипа
        tooltip = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".highcharts-tooltip")
        ))
        tooltip_text = tooltip.text.strip()
        print("Текст тултипа:", tooltip_text)

        # 5. Проверяем содержимое тултипа
        assert "commits" in tooltip_text.lower(), \
            f"В тултипе нет слова 'commits': {tooltip_text!r}"
        assert "week of" in tooltip_text.lower(), \
            f"В тултипе нет 'week of': {tooltip_text!r}"

        # Число коммитов может идти и до, и после слова "Commits"
        m = (re.search(r"(\d+)\s*commits", tooltip_text, re.IGNORECASE)
             or re.search(r"commits\s+(\d+)", tooltip_text, re.IGNORECASE))
        assert m, f"Не нашли число коммитов в тултипе: {tooltip_text!r}"

        commits = int(m.group(1))
        print(f"Коммитов за неделю: {commits}")
        assert commits > 0, f"Число коммитов должно быть > 0, а не {commits}"

        print("Тултип содержит ожидаемые значения ✅")

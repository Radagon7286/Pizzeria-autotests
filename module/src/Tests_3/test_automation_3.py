import re
import allure
from playwright.sync_api import Page, expect


@allure.feature('Full Account')
@allure.story('Waiting page load')
class TestCases3:

    @allure.title('Поиск задач со словом "bug"')
    def test_1(self, page: Page):
        with allure.step('Открываем страницу'):
            page.goto("https://github.com/microsoft/vscode/issues")

        with allure.step('Вводим поисковый запрос в поле поиска'):
            search_input = page.locator("#issues-index-filter-input")
            search_input.click()
            search_input.fill("in:title bug")
            search_input.press("Enter")

        with allure.step('Ждём появления заголовков задач'):
            title_locator = 'a[href*="/microsoft/vscode/issues/"]'
            # Ждём, что появится хотя бы один заголовок
            expect(page.locator(title_locator).first).to_be_visible()

        with allure.step('Собираем тексты заголовков'):
            titles = []
            for el in page.locator(title_locator).all():
                text = (el.inner_text() or "").strip()
                if text and not text.lstrip("#").isdigit():
                    titles.append(text)

        print(f"Найдено задач: {len(titles)}")

        with allure.step('Проверяем, что поиск вернул результаты'):
            assert len(titles) > 0, "Поиск не вернул ни одной задачи"
        print(f"✅ Найдено {len(titles)} задач по запросу 'in:title bug'")

    @allure.title('Поиск элемента "bpasero" с помощью дропдауна')
    def test_2(self, page: Page):
        with allure.step('Открываем страницу'):
            page.goto('https://github.com/microsoft/vscode/issues')

        with allure.step('Открываем страницу и нажимаем на кнопку "author"'):
            page.locator("button[aria-label='Filter by author']").click()

        with allure.step('Ввод имени: "bpasero"'):
            el_input = page.locator("input[placeholder='Filter authors']")
            el_input.wait_for(state="visible")
            el_input.fill("bpasero")

        with allure.step('Выбор пункта author:"bpasero"'):
            page.locator(
                "//li[@role='option'][.//*[contains(text(), 'author:bpasero')]]"
            ).click()

        with allure.step('Ждём, что фильтр применился'):
            page.wait_for_url(re.compile(r".*bpasero.*"))

        with allure.step('Получаем все задачи'):
            title_css = 'a[href*="/microsoft/vscode/issues/"]'
            page.locator(title_css).first.wait_for(state="visible")
            titles = [
                (el.inner_text() or "").strip()
                for el in page.locator(title_css).all()
                if (el.inner_text() or "").strip()
            ]
            assert titles, "Список задач пуст — фильтр не сработал?"

        with allure.step('Проверка, что фильтр по автору "bpasero" применился'):
            assert "bpasero" in page.url, \
                f"В URL нет фильтра по автору: {page.url}"

    @allure.title('Поиск репозитория по заданым критериям')
    def test_3(self, page: Page):
        with allure.step('Открываем страницу'):
            page.goto('https://github.com/search/advanced')

        with allure.step('Выбор языка Python'):
            page.locator("#search_language").select_option(value="Python")

        with allure.step('Звёзды'):
            el_stars = page.locator("#search_stars")
            el_stars.click()
            el_stars.fill(">20000")

        with allure.step('Имя файла'):
            el_file_name = page.locator("#search_filename")
            el_file_name.click()
            el_file_name.fill("environment.yml")

        with allure.step('Кнопка поиска'):
            el_button = page.locator("#adv_code_search button[type='submit'].btn")
            el_button.scroll_into_view_if_needed()
            el_button.click()

        with allure.step('Ждём загрузки результатов'):
            page.locator('a[href$="/stargazers"]').first.wait_for(state="visible")

        with allure.step('Собираем звёзды у каждой карточки'):
            star_links = page.locator('a[href$="/stargazers"]')
            raw_aria = [
                star_links.nth(i).get_attribute("aria-label")
                for i in range(star_links.count())
            ]
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
    def test_4(self, page: Page):
        with allure.step('Открываем страницу по заданному разрешению'):
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto('https://skillbox.ru/code/')

        with allure.step('Вкладка «Профессия»'):
            page.locator("//button[normalize-space()='Профессия']").click()

        with allure.step('Длительность → «От 6 до 12 мес.»'):
            page.locator(
                "//button[contains(@class, 'ui-round-select__field') "
                "and contains(normalize-space(.), 'Длительность')]"
            ).click()
            page.locator(
                "//li[contains(@class, 'ui-round-select__item') "
                "and normalize-space()='От 6 до 12 мес.']"
            ).click()

        with allure.step('Тематика → первая доступная'):
            tematika_btn = page.locator(
                "//button[contains(@class, 'ui-round-select__field') "
                "and contains(normalize-space(.), 'Тематика')]"
            )

        with allure.step('Скроллим к кнопке «Тематика»'):
            tematika_btn.scroll_into_view_if_needed()

        with allure.step('Кликаем по кнопке «Тематика»'):
            tematika_btn.click()
            print("✅ Кликнули по кнопке 'Тематика'")

        with allure.step('Ждём появления списка опций'):
            options = page.locator(
                'ul.ui-round-select__list li.ui-round-select__item'
            )
            options.first.wait_for(state="visible")
            print(f"Найдено опций в списке 'Тематика': {options.count()}")

        with allure.step('Выбираем первую видимую опцию «Тематика»'):
            picked = False
            for i in range(options.count()):
                opt = options.nth(i)
                if opt.is_visible():
                    text = (opt.inner_text() or "").strip()
                    print(f"Кликаем по опции: {text!r}")
                    opt.click()
                    picked = True
                    break
            assert picked, "Не нашли ни одной видимой опции в списке 'Тематика'"

        with allure.step('Ждём, что фильтр применился (URL содержит duration_min)'):
            page.wait_for_url(re.compile(r".*duration_min.*"))

        with allure.step('Ждём появления карточек профессий'):
            card_css = 'li.product-card-new__feature'
            page.locator(card_css).first.wait_for(state="visible")

        with allure.step('Собираем длительности из карточек'):
            features = page.locator(card_css)
            print(f"Найдено feature-элементов: {features.count()}")

            durations_months = []
            for i in range(features.count()):
                txt = (features.nth(i).inner_text() or "").strip()
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
            assert not bad, f"Найдены длительности вне диапазона 6–12 мес.: {bad}"

        with allure.step('Финальная проверка пройдена'):
            print(f"✅ Все {len(durations_months)} длительностей "
                  f"в диапазоне 6–12 мес. ✅")

    @allure.title('Проверка тултипа графика коммитов')
    def test_5(self, page: Page):
        with allure.step('Открываем страницу по заданному разрешению'):
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto('https://github.com/microsoft/vscode/graphs/commit-activity')

        with allure.step('Ждём столбики'):
            bars = page.locator(".highcharts-column-series path")
            bars.first.wait_for(state="visible")
            assert bars.count() > 0, "Не нашли столбики графика"
            print(f"Найдено столбиков: {bars.count()}")

        with allure.step('Берём последний столбик (свежая неделя)'):
            last_index = bars.count() - 1
            bar = bars.nth(last_index)

        with allure.step('Читаем эталон из aria-label столбика'):
            aria_label = bar.get_attribute("aria-label")
        print(f"aria-label столбика: {aria_label!r}")
        assert aria_label, "У столбика нет aria-label"

        m_ref = re.search(r"(\d[\d,]*)\s*[.,]?\s*Commits", aria_label, re.IGNORECASE)
        assert m_ref, f"Не нашли число коммитов в aria-label: {aria_label!r}"
        expected_commits = int(m_ref.group(1).replace(",", ""))
        print(f"Эталонное число коммитов: {expected_commits}")

        with allure.step('Наводим мышку'):
            bar.hover()

        with allure.step('Ждём тултип'):
            tooltip = page.locator(".highcharts-tooltip")
            tooltip.wait_for(state="visible")
            tooltip_text = (tooltip.text_content() or "").strip()
        print("Текст тултипа:", repr(tooltip_text))

        with allure.step('Проверяем содержимое'):
            assert "commits" in tooltip_text.lower(), \
                f"В тултипе нет слова 'commits': {tooltip_text!r}"
            assert "week of" in tooltip_text.lower(), \
                f"В тултипе нет 'week of': {tooltip_text!r}"

        with allure.step('Парсим число после слова "Commits"'):
            m = re.search(r"Commits\s*(\d[\d,]*)", tooltip_text, re.IGNORECASE)
        assert m, f"Не нашли число коммитов в тултипе: {tooltip_text!r}"

        actual_commits = int(m.group(1).replace(",", ""))
        print(f"Число из тултипа: {actual_commits}")

        with allure.step('ГЛАВНАЯ ПРОВЕРКА: сравниваем конкретные значения'):
            assert actual_commits == expected_commits, (
                f"Тултип показывает {actual_commits}, "
                f"а в aria-label столбика {expected_commits} — значения не совпадают"
            )

        print("✅ Тултип содержит корректное значение ✅")
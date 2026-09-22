import allure


@allure.step('Проверка заголовка страницы')
def check_title(driver, title: str):
    assert title == driver.title


class TestExample:


    def test_example(self, set_up_browser):
        driver = set_up_browser
        driver.get("https://Skillbox.ru")
        check_title(driver=driver, title='Skillbox – образовательная платформа с онлайн-курсами.')


    def test_example1(self, set_up_browser):
        driver = set_up_browser
        driver.get("https://Skillbox.ru")
        assert 'Skillbox' == driver.title


    def test_example2(self, set_up_browser):
        driver = set_up_browser
        driver.get("https://Skillbox.ru")
        assert 'Skillbox' == driver.title


    def test_example3(self, set_up_browser):
        driver = set_up_browser
        driver.get("https://Skillbox.ru")
        assert 'Skillbox' == driver.title
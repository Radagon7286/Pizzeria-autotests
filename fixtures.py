import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging.config
import logging


@pytest.fixture
def selenium():
    options = Options()
    options.set_capability("browserVersion", "latest")
    options.set_capability("platformName", "windows")
    logging.info(f"options: {options}")

    # Автоматически скачает и установит ChromeDriver
    service = Service(ChromeDriverManager().install())
    selenium = webdriver.Chrome(service=service, options=options)
    logging.info(f"selenium: {selenium}")

    yield selenium

    selenium.quit()
    logging.info("Браузер успешно закрыт")

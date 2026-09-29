import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging.config
from os import  path
import logging


project_root = path.dirname(path.dirname(path.abspath(__file__)))
lof_file_path = path.join(project_root, 'logging.ini')
logging.config.fileConfig(lof_file_path)


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
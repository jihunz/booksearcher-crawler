from contextlib import asynccontextmanager

from selenium import webdriver


class WebDriverManager:
    @classmethod
    def get_driver(cls):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        return driver
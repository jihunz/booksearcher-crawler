from selenium import webdriver

from util.proxy_manager import Proxy_manager


class Webdriver_util:
    @classmethod
    def create_driver(cls):
        proxy = Proxy_manager.get_proxy()['http']
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--proxy-server=%s' % proxy)

        # 웹드라이버 생성
        return webdriver.Chrome(options=options)

from selenium import webdriver
from util.proxy_manager import Proxy_manager
import requests



class Webdriver_creator:
    @classmethod
    def get_driver(cls):
        proxy_map = None

        proxy_not_found = True
        while proxy_not_found:
            proxy_list = Proxy_manager.proxy_result_list
            if proxy_list:
                proxy_map = proxy_list[0]
                proxy_not_found = False
                print('[WEBDRIVER_MANAGER]: proxy found')

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--proxy-server=%s' % proxy_map['http'])

        # 웹드라이버 생성
        driver = webdriver.Chrome(options=options)

        return driver

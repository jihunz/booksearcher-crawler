import random
import time

from util import html_manager
import requests
from user_agent import generate_user_agent


class Proxy_manager:
    proxy_result_list = []
    url = 'https://www.sslproxies.org'
    target_url = 'https://www.u-library.kr/'
    headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}

    @classmethod
    def get_proxy(cls):
        soup = html_manager.parse_html(cls.url)
        proxy_list = soup.find('table', class_='table table-striped table-bordered').find_all('tr')[1:]
        proxy_result_list_len = len(cls.proxy_result_list)
        max_size = 10

        while True:
            print('[PROXY_RESULT_LIST]: ', proxy_result_list_len, '/', max_size)
            if proxy_result_list_len >= max_size:
                break

            print('[PROXY]: finding proxy')
            try:
                rand_num = random.randint(0, (len(proxy_list) - 70))
                tds = proxy_list[rand_num].find_all('td')
                proxy_url = tds[0].text + ':' + tds[1].text
                proxy = {
                    'http': 'http://' + proxy_url,
                    'https': 'http://' + proxy_url,
                }
                requests.get(cls.target_url, headers=cls.headers, proxies=proxy, timeout=1)
                print('[PROXY-SUCCESS]: ' + proxy_url)
                cls.proxy_result_list.append(proxy)
            except Exception as e:
                print('[PROXY-FAIL]: ' + str(e))

    @classmethod
    def chk_proxy(cls):
        while True:
            for i in range(0, len(cls.proxy_result_list)):
                try:
                    requests.get(cls.target_url, headers=cls.headers, proxies=cls.proxy_result_list[i], timeout=5)
                    print('[PROXY-CHK-SUCCESS]')
                except Exception as e:
                    print('[PROXY-CHK-FAIL]: ' + str(e))
                    del cls.proxy_result_list[i]

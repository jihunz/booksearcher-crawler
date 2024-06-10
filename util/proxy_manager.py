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
        proxy_num = 0
        # max_size = 10
        proxy_not_founded = True
        # while len(cls.proxy_result_list) < max_size:
        while proxy_not_founded:
            try:
                # rand_num = random.randint(0, (len(proxy_list) - 70))
                td = proxy_list[proxy_num].find_all('td')
                print(proxy_num)
                proxy_url = td[0].text + ':' + td[1].text
                proxy = {
                    'http': 'http://' + proxy_url,
                    'https': 'http://' + proxy_url,
                }
                requests.get(cls.target_url, headers=cls.headers, proxies=proxy, timeout=2)
                cls.proxy_result_list.append(proxy)
                print('[PROXY-MANAGER] Success: ' + proxy_url)
                # print('[PROXY-MANAGER] List size: ', len(cls.proxy_result_list), '/', max_size)
                proxy_not_founded = False
                return proxy
            except Exception as e:
                proxy_num += 1
                print('[PROXY-MANAGER] Fail: ' + str(e))

    # @classmethod
    # def chk_proxy(cls):
    #     while True:
    #         for i in range(0, len(cls.proxy_result_list)):
    #             proxy_item = cls.proxy_result_list[i]
    #             try:
    #                 requests.get(cls.target_url, headers=cls.headers, proxies=proxy_item, timeout=5)
    #             except Exception as e:
    #                 print('[PROXY-MANAGER] Chk fail -> delete: ', proxy_item)
    #                 if len(cls.proxy_result_list) > 0:
    #                     del proxy_item

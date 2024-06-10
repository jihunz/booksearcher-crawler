from config import get_config
from util import html_manager
import requests
from user_agent import generate_user_agent


class Proxy_manager:
    url = get_config().PROXY_SOURCE_URL
    target_url = get_config().TARGET_URL
    headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}

    @classmethod
    def get_proxy(cls):
        soup = html_manager.parse_html(cls.url)
        proxy_list = soup.find('table', class_='table table-striped table-bordered').find_all('tr')[1:]
        proxy_num = 0
        proxy_not_founded = True
        while proxy_not_founded:
            try:
                td = proxy_list[proxy_num].find_all('td')
                print(proxy_num)
                proxy_url = td[0].text + ':' + td[1].text
                proxy = {
                    'http': 'http://' + proxy_url,
                    'https': 'http://' + proxy_url,
                }
                requests.get(cls.target_url, headers=cls.headers, proxies=proxy, timeout=2)
                print('[PROXY-MANAGER] Success: ' + proxy_url)
                proxy_not_founded = False
                return proxy
            except Exception as e:
                proxy_num += 1
                print('[PROXY-MANAGER] Fail: ' + str(e))
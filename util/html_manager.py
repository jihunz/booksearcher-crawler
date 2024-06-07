from user_agent import generate_user_agent
from bs4 import BeautifulSoup as bs
import requests


def send_req(url, proxyUrl):
    if proxyUrl:
        headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}
        return requests.get(url, headers=headers, proxies=proxyUrl)
    else:
        return requests.get(url)


def parse_html_proxy(url, proxyUrl):
    request = send_req(url, proxyUrl)
    return bs(request.text, 'html.parser')


def parse_html(url):
    request = send_req(url, False)
    return bs(request.text, 'html.parser')


def parse_lxml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
    request = requests.get(url, headers=headers)
    return bs(request.content, 'lxml')
import time
import traceback

from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait

from config import get_config
from util import html_manager
from util.proxy_manager import Proxy_manager
from .webdriver_util import Webdriver_util as wdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Crawler_service:
    @classmethod
    async def exec_crawl(cls, term: str):
        try:
            result = {}
            url = get_config().get_search_url(term)
            # proxy = Proxy_manager.get_proxy()
            await cls.crawl_pages(url, result)

            return result
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    @classmethod
    async def crawl_book(cls, soup, result):
        li_list = soup.select('.resultList li')

        for item in li_list:
            dd_list = item.select("dl dd")
            title = dd_list[3].find('a').get_text()
            code = dd_list[6].get_text()
            a = dd_list[-1].find('a')
            status = a.find('span').get_text()
            library = a.get_text().replace(status, '')

            if '대출가능' not in status and '대출중' not in status:
                continue

            if library not in result:
                result[library] = []

            result[library].append({
                'title': title,
                'code': code,
                'library': library,
                'status': status
            })

    @classmethod
    async def crawl_pages(cls, url, result):
        base_url = 'https://www.u-library.kr/search/tot/result'
        # soup = html_manager.parse_html_proxy(url, proxy)
        soup = html_manager.parse_html(url)

        if soup.find('div', id='divNoResult'):
            return

        a = soup.select('.paging span a')
        last_a = int(a[-1].get_text()) if a else 1
        curr_page = int(soup.select('.paging span span')[0].get_text())
        last_page = last_a if curr_page < last_a else curr_page

        print(f'[CRAWLER-PAGE-{curr_page}]: {url}')

        await cls.crawl_book(soup, result)

        if last_page == 1:
            return

        if curr_page < last_page:
            next_page_url = base_url + soup.find('a', text=str(curr_page + 1)).get('href')
            await cls.crawl_pages(next_page_url, result)
        elif curr_page == last_page:
            next_grp_btn = soup.select('.paging > a[title="다음"]')
            if len(next_grp_btn) > 0:
                next_grp_url = base_url + next_grp_btn[0].get('href')
                print('[CRAWLER-NEXT GROUP]')
                await cls.crawl_pages(next_grp_url, result)

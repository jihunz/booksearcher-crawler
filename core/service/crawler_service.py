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
    crawled_url_dic = {}

    @classmethod
    async def exec_crawl(cls, term: str):
        # TODO: 검색 결과 없을 때 크롤링 조기 리턴
        try:
            result = []
            url = get_config().get_search_url(term)
            # driver = wdm.create_driver()
            # driver.get(url)
            # await cls.crawl2(driver, result, 0)
            # proxy = Proxy_manager.get_proxy()
            await cls.crawl(url, result)

            # driver.quit()
            return result
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    @classmethod
    async def crawl_book_chk_info(cls, driver, result):
        li_list = driver.find_element(By.CLASS_NAME, 'resultList').find_elements(By.TAG_NAME, "li")
        for item in li_list:
            dd_list = item.find_elements(By.CSS_SELECTOR, "dl dd")
            title = dd_list[3].find_element(By.TAG_NAME, "a").text
            call_num = dd_list[6].text
            a = dd_list[-1].find_element(By.CSS_SELECTOR, "a")
            library = a.text
            check_availability = a.find_element(By.CSS_SELECTOR, "span").text

            if '대출불가' in check_availability:
                continue

            result.append({
                'title': title,
                'call_num': call_num,
                'library': library.replace(check_availability, ''),
                'check_availability': check_availability
            })

    @classmethod
    async def crawl(cls, url, result):
        base_url = 'https://www.u-library.kr/search/tot/result'
        # soup = html_manager.parse_html_proxy(url, proxy)
        soup = html_manager.parse_html(url)

        if soup.find('div', id='divNoResult'):
            return

        a = soup.select('.paging span a')
        last_a = int(a[-1].get_text()) if a else 1
        curr_page = int(soup.select('.paging span span')[0].get_text())
        last_page = last_a if curr_page < last_a else curr_page

        print(curr_page)

        # TODO: 크롤링

        if last_page == 1:
            return

        if curr_page < last_page:
            next_page_url = base_url + soup.find('a', text=str(curr_page + 1)).get('href')
            # TODO: 크롤링
            await cls.crawl(next_page_url, result)
        elif curr_page == last_page:
            next_grp_btn = soup.select('.paging > a[title="다음"]')
            if len(next_grp_btn) > 0:
                next_grp_url = base_url + next_grp_btn[0].get('href')
                await cls.crawl(next_grp_url, result)

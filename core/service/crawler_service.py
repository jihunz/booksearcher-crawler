import time
import traceback

from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait

from config import get_config
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
            driver = wdm.create_driver()
            driver.get(get_config().get_search_url(term))

            await cls.crawl2(driver, result, 0)

            driver.quit()
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
    async def crawl(cls, driver, result, idx=0):
        await cls.crawl_book_chk_info(driver, result)

        a = driver.find_elements(By.CSS_SELECTOR, '.paging span a')
        if len(a) == 0:
            return

        driver.get(a[idx].get_attribute('href'))
        await cls.crawl_book_chk_info(driver, result)

        if idx == len(a) - 1:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.paging > a[title="다음"]')))
            next = driver.find_elements(By.CSS_SELECTOR, '.paging > a[title="다음"]')

            if len(next) == 0:
                print('다음 페이지 크롤링')
                driver.get(next[0].get_attribute('href'))
                await cls.crawl(driver, result, idx + 1)

    @classmethod
    async def crawl2(cls, driver, result, idx):
        # 페이지네이션을 위해 마지막 페이지 탐색
        final_page = None
        a = driver.find_elements(By.CSS_SELECTOR, '.paging span a')
        for i in range(len(a)):
            if i == len(a) - 1:
                final_page = int(a[i].text)

        # 다음 페이지 크롤링 -> 재귀 -> 인덱스 증가? 새로운 페이지 선택 -> get -> 크롤링
        await cls.crawl_book_chk_info(driver, result)

        if len(a) == 0:
            return

        print(final_page) # TODO: 현재 페이지= span / a=final_page라면 현재 페이지=5일때 a=4
        if idx < final_page:
            next_page = idx + 1
            driver.get(a[next_page].get_attribute('href'))
            await cls.crawl2(driver, result, next_page)
        elif idx == final_page:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.paging > a[title="다음"]')))
            next = driver.find_elements(By.CSS_SELECTOR, '.paging > a[title="다음"]')

            if len(next) > 0:
                print('다음 페이지 크롤링')
                driver.get(next[0].get_attribute('href'))
                await cls.crawl2(driver, result, idx + 1)

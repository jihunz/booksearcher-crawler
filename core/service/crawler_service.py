import time
import traceback

from fastapi import Depends
from loguru import logger
from .webdriver_manager import WebDriverManager as wdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler_service:

    @classmethod
    async def crawl(cls, term: str):
        try:
            result_list = []
            driver = wdm.get_driver()
            try:
                driver.get("https://www.u-library.kr/")
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))

                search_input = driver.find_element(By.XPATH, '//*[@id="search"]')
                search_input.send_keys(term)
                search_input.submit()

                per_page = driver.find_element(By.XPATH, '//*[@id="searchOption"]/fieldset/a[3]/span[1]')
                driver.execute_script("arguments[0].innerText = '100';", per_page)
                driver.find_element(By.XPATH, '//*[@id="searchOption"]/fieldset/input[4]').submit()

                # page_list = driver.find_element(By.CSS_SELECTOR, 'div .paging > span').find_elements(By.TAG_NAME, 'a')

                page = 1

                while True:
                    await cls.exec_crawl(driver, page, result_list)

                # time.sleep(2)

                # for i in range(0, len(page_list)):
                #     await cls.crawl_chk_info(driver, result_list)
                #     page_list[i].click()

                # if next_page_num > len(page_list) - 1:
                #     next = driver.find_element(By.XPATH,
                #                                '//*[@id="divContent"]/div/div[3]/div[2]/form/fieldset/div/a[1]')
                #     if next:
                #         next.click()

                return result_list
            finally:
                time.sleep(3)
                driver.quit()
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    @classmethod
    async def exec_crawl(cls, driver, page, result_list):
        last_page = int(driver.find_element(By.CSS_SELECTOR, '.paging').text[-1])
        await cls.crawl_chk_info(driver, result_list)
        if page < last_page:
            next_page = driver.find_element(By.LINK_TEXT, str(page + 1))
            next_page.click()
            page += 1
        elif page == last_page and driver.find_element(By.CSS_SELECTOR, 'img[title="다음'):
            driver.find_element(By.CSS_SELECTOR, 'a[title="다음').click()
            await cls.exec_crawl(driver, page, result_list)

    @classmethod
    async def crawl_chk_info(cls, driver, result_list):
        li_list = driver.find_element(By.CLASS_NAME, 'resultList').find_elements(By.TAG_NAME, "li")
        for item in li_list:
            dd_list = item.find_elements(By.CSS_SELECTOR, "dl dd")
            title = dd_list[3].find_element(By.TAG_NAME, "a").text
            call_num = dd_list[6].text
            a = dd_list[-1].find_element(By.CSS_SELECTOR, "a")
            library = a.text
            check_availability = a.find_element(By.CSS_SELECTOR, "span").text

            result_list.append({
                'title': title,
                'call_num': call_num,
                'library': library.replace(check_availability, ''),
                'check_availability': check_availability
            })

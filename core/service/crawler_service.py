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
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))

                search_input = driver.find_element(By.XPATH, '//*[@id="search"]')
                search_input.send_keys(term)
                search_input.submit()
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

                return result_list
            finally:
                driver.quit()
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

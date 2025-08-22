import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scraper_log = logging.getLogger('selenium')
scraper_log.setLevel(logging.ERROR)


class BaseScraper:
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, url):
        try:
            scraper_log.info(f"導航到: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            scraper_log.error(f"導航失敗: {e}")
            return False

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            scraper_log.warning(f"找不到元素: {value}")
            return None

    def wait_for_element_clickable(self, by, value, timeout):
        try:
            wait = WebDriverWait(self.driver, timeout, 1).until(
                EC.presence_of_element_located((by, value))
            )
            return wait
        except TimeoutException:
            scraper_log.error(f"等待元素可點擊超時: {value}")
            return None

    def handle_over18(self):
        try:
            btn = self.driver.find_element(By.XPATH, '//button[@value="yes"]')
            btn.click()
            scraper_log.info("已確認18歲")
            return True
        except NoSuchElementException:
            # 沒有跳出18歲頁，正常流程
            return False

    @staticmethod
    def click_element(element):
        element.click()
        return True


class Scraper(BaseScraper):
    def __init__(self, driver):
        super().__init__(driver)

    def scrape_ptt(self):
        try:
            # 到指定url
            self.navigate('https://www.ptt.cc/bbs/index.html')

            raw_board_xpath = '''//*[@id="main-container"]/div[2]/div[]/a'''
            board_xpath = raw_board_xpath[:37] + '1' + raw_board_xpath[37:]

            # 等待元素載入出來(之後用for loop包起來)
            is_load = self.wait_for_element_clickable(By.XPATH, board_xpath, 10)
            if not is_load:
                scraper_log.error('找不到看板')
                return []

            # 定位元素並點擊
            tech_job_entry_bottom = self.find_element(By.XPATH, board_xpath)
            self.click_element(tech_job_entry_bottom)

            # 未滿18歲頁面
            self.handle_over18()

        except Exception as e:
            scraper_log.error(f"爬取過程中發生錯誤: {e}")
            return []


'''
//*[@id="main-container"]/div[2]/div[1]/a
//*[@id="main-container"]/div[2]/div[2]/a
//*[@id="main-container"]/div[2]/div[3]/a
'''

webdriver = webdriver.Chrome()
scraper = Scraper(webdriver)

scraper.scrape_ptt()
time.sleep(10)

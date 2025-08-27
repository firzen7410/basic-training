from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BaseScraper:
    def __init__(self, driver, scraper_log):
        self.driver = driver
        self.scraper_log = scraper_log

    def navigate(self, url):
        try:
            self.scraper_log.info(f"導航到: {url}")
            self.driver.get(url)
            return True
        except Exception as e:
            self.scraper_log.error(f"導航失敗: {e}")
            return False

    def get_page_source(self):
        html = self.driver.page_source
        return html

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            self.scraper_log.warning(f"找不到元素: {value}")
            return None

    def wait_for_element(self, by, value, timeout):
        try:
            wait = WebDriverWait(self.driver, timeout, 1).until(
                EC.presence_of_element_located((by, value))
            )
            return wait
        except TimeoutException:
            self.scraper_log.error(f"等待元素可點擊超時: {value}")
            return None

    def handle_over18(self):
        try:
            btn = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[1]/button')
            btn.click()
            self.scraper_log.info("已確認18歲")
            return True
        except NoSuchElementException:
            # 沒有跳出18歲頁，正常流程
            return False

    def back(self):
        try:
            self.driver.back()
        except NoSuchElementException:
            self.scraper_log.error("按上一頁失敗")
            return False

    @staticmethod
    def click_element(element):
        element.click()
        return True

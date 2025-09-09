import time
from datetime import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from stage3.scrapper.database_handler import DatabaseHandler


class BaseScraper:
    def __init__(self, driver, scraper_log):
        self.driver = driver
        self.scraper_log = scraper_log
        self.db_handler = DatabaseHandler(self.scraper_log)

    def _log(self, task_name, status, message, level="INFO"):
        log_data = {
            "task_name": task_name,
            "status": status,
            "message": message,
            "level": level,
            "execute_at": datetime.now()
        }
        self.db_handler.insert_log(log_data)

        # 同步寫進 scraper_log
        getattr(self.scraper_log, level.lower())(message)

    def navigate(self, url):
        try:
            self.driver.get(url)
            self._log("導航", "success", f"導航到{url}", "DEBUG")
            return True
        except Exception as e:
            self._log("導航", "failed", f"導航失敗:{e}", "ERROR")
            return False

    def get_page_source(self):
        html = self.driver.page_source
        return html

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            self._log(f"find_element:{value}", "failed", "ERROR:找不到該元素", "ERROR")
            return None

    def wait_for_element(self, by, value, timeout):
        try:
            wait = WebDriverWait(self.driver, timeout, 1).until(
                EC.presence_of_element_located((by, value))
            )
            return wait
        except TimeoutException:
            self._log(f"wait_for_element:{value}", "failed", "ERROR:等待元素超時", "ERROR")
            self.back()
            return None

    def move_to_element(self, element):
        if element is None:
            self.scraper_log.warning("move_to_element: element 為 None")
            return False
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            time.sleep(3)  # 稍微等一下捲動完成
            return True
        except Exception as e:
            self._log(f"move_to_element:{element}", f"failed:{e}", "捲動到該元素失敗", "ERROR")
            return False

    def handle_over18(self):
        try:
            time.sleep(1)
            btn = self.driver.find_element(By.XPATH, '/html/body/div[2]/form/div[1]/button')
            btn.click()
            self._log("handle_over18", "success", "已點擊成功")
            return True
        except NoSuchElementException:
            # 沒有跳出18歲頁，正常流程
            return False

    def back(self):
        try:
            self.driver.back()
        except NoSuchElementException:
            self._log("按上一頁", "failed", "該元素不存在", "ERROR")
            return False

    @staticmethod
    def click_element(element):
        element.click()
        return True

    @staticmethod
    def safe_to_text(element, default=""):
        """
        安全地將 Selenium WebElement 或 BeautifulSoup Tag 轉成文字。
        如果 element 為 None 或沒有 text 屬性，回傳預設值。
        """
        try:
            return element.text.strip() if element and hasattr(element, "text") else default
        except Exception:
            return default

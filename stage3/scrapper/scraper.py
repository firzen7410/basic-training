import time
from datetime import datetime
<<<<<<< HEAD

=======
>>>>>>> 4f4dad3 ('重置')
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from stage3.scrapper.base_scraper import BaseScraper
from stage3.scrapper.parser_handler import PttParser


class Scraper(BaseScraper):
    def __init__(self, driver, scraper_log, db_handler):
        super().__init__(driver, scraper_log)
        self.scraper_log = scraper_log
        self.db_handler = db_handler

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

    def scrape_ptt(self, board, max_runtime=60 * 59):
        start_time = time.time()
        try:
            # 到指定url
            self.navigate('https://www.ptt.cc/bbs/index.html')

            # 等待看板頁面載入
            is_load = self.wait_for_element(By.CSS_SELECTOR, '.b-list-container.action-bar-margin.bbs-screen', 10)
            if not is_load:
                return []

            # 找到指定看板
            ptt_boards = self.driver.find_elements(By.CLASS_NAME, 'board-name')
            found_board = False
            for each in ptt_boards:
                if self.safe_to_text(each) == board:
                    each.click()
                    found_board = True
                    break

            if not found_board:
                return []  # 找不到板就結束

            # 未滿18歲頁面
            self.handle_over18()

            # 等文章列表頁面載入出來
            self.wait_for_element(By.XPATH, '//*[@id="main-container"]/div[2]', 10)

            while True:
                # 檢查時間是否超過 max_runtime
                if time.time() - start_time > max_runtime:
                    self._log("檢查時間是否超過 max_runtime", "success",
                              "f{board} 爬蟲已執行 {max_runtime / 60:.0f} 分鐘，自動停止", "WARNING")
                    break

                # 分隔線之下是板規、公告，不抓
                sep = self.driver.find_elements(By.CLASS_NAME, 'r-list-sep')
                if sep:
                    articles = self.driver.find_elements(
                        By.XPATH, '//div[@class="r-list-sep"]/preceding-sibling::div[@class="r-ent"]'
                    )
                else:
                    articles = self.driver.find_elements(By.CLASS_NAME, 'r-ent')
                articles = list(reversed(articles))

                # 進到文章列表
                for art in articles:
                    if time.time() - start_time > max_runtime:
                        break
                    try:
                        link_elements = art.find_elements(By.TAG_NAME, "a")

                        if not link_elements:
                            # 沒有 <a> 連結 → 文章被刪除或無法點
                            self._log("文章狀態", "deleted", "該文章已被刪除或無連結可點")
                            continue

                        # 有 <a>，正常抓取文章
                        link = link_elements[0]
                        url = link.get_attribute("href")
                        self.driver.get(url)  # 直接跳轉

                        # 等待文章主頁加載出來
                        is_load = self.wait_for_element(By.XPATH, '//*[@id="main-content"]', 10)
                        if is_load:
                            html = self.get_page_source()
                            parser = PttParser(self.driver, self.scraper_log)

                            # insert posts
                            post_data = parser.parse_post(html)
                            self.db_handler.insert_post(post_data)

                            # insert comments
                            comment_data = parser.parse_comment(html)
                            if comment_data:
                                self.db_handler.insert_comment(comment_data)

                            self.back()
                    except Exception as e:
                        self._log("scraper:文章列表內發生錯誤", "failed", f"{e}", "ERROR")

                # 爬完一頁，等待 <上頁> 元素載入
                is_load = self.wait_for_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]', 6)
                if is_load:
                    find_old_bottom = self.find_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]')
                    self.click_element(find_old_bottom)

        except Exception as e:
            self._log("scraper:爬取流程發生錯誤", "failed", f"{e}", "ERROR")
            return []
        finally:
            try:
                self.driver.quit()
                self._log("結束流程", "success", f"{board} driver 已正常關閉")
            except Exception as e:
                self._log("結束流程", "failed", f"driver.quit() 失敗: {e}", "ERROR")

import time
from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from parser_handler import PttParser


class Scraper(BaseScraper):
    def __init__(self, driver, scraper_log, db_handler):
        super().__init__(driver, scraper_log)
        self.scraper_log = scraper_log
        self.db_handler = db_handler

    def scrape_ptt(self):
        try:
            # 到指定url
            self.navigate('https://www.ptt.cc/bbs/index.html')

            # 看板xpath
            board_index = 1
            board_xpath = f'//*[@id="main-container"]/div[2]/div[{board_index}]/a'

            # 等待元素載入出來(之後用for loop包起來)
            is_load = self.wait_for_element(By.XPATH, board_xpath, 10)
            if not is_load:
                self.scraper_log.error('找不到看板')
                return []

            # 定位元素並點擊
            tech_job_entry_bottom = self.find_element(By.XPATH, board_xpath)
            self.click_element(tech_job_entry_bottom)

            # 未滿18歲頁面
            self.handle_over18()
            while True:
                # 進到文章列表，一個頁面有20篇，從21~2，新到舊
                for i in range(21, 2, -1):
                    print(i)
                    article_xpath = f'//*[@id="main-container"]/div[2]/div[{i}]/div[2]/a'
                    is_load = self.wait_for_element(By.XPATH, article_xpath, 10)

                    if not is_load:
                        self.scraper_log.info("此文章不在頁面或已被刪除，跳過")
                    else:
                        # 進到文章頁面
                        article_element = self.find_element(By.XPATH, article_xpath)
                        self.click_element(article_element)

                        # 等待文章主頁加載出來
                        is_load = self.wait_for_element(By.XPATH, '//*[@id="main-content"]', 10)
                        if is_load:
                            # 交給beautifulsoup解析
                            html = self.get_page_source()
                            post_data = PttParser.parse_post(html, self.driver)
                            # 將表格資料插入
                            self.db_handler.insert_post(post_data)
                        self.back()
                        # //*[@id="main-container"]/div[2]/div[2]/div[2]/a
                # 爬完一頁，按<上頁
                is_load = self.wait_for_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]', 10)
                if is_load:
                    find_old_bottom = self.find_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]')
                    self.click_element(find_old_bottom)


        except Exception as e:
            self.scraper_log.error(f"爬取過程中發生錯誤: {e}")
            return []

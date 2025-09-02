import time
from selenium.webdriver.common.by import By
from stage3.scrapper.base_scraper import BaseScraper
from stage3.scrapper.parser_handler import PttParser


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

            # 等文章列表頁面載入出來
            self.wait_for_element(By.XPATH, '//*[@id="main-container"]/div[2]', 10)

            while True:
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
                    try:
                        # 判斷是否被刪文
                        title_text = art.find_element(By.CLASS_NAME, 'title').text
                        if "本文已被刪除" in title_text:
                            self.scraper_log.info("本文已被刪除")
                            continue  # 跳過這篇文章
                        else:
                            self.move_to_element(art.find_element(By.TAG_NAME, 'a'))
                            art.find_element(By.TAG_NAME, "a").click()

                            # 等待文章主頁加載出來
                            is_load = self.wait_for_element(By.XPATH, '//*[@id="main-content"]', 10)
                            if is_load:
                                # 交給beautifulsoup解析
                                html = self.get_page_source()

                                # 解析posts欄位所需資料
                                parser = PttParser(self.driver, self.scraper_log)
                                post_data = parser.parse_post(html)

                                # 將資料插入posts
                                self.db_handler.insert_post(post_data)

                                # 解析comment欄位所需資料
                                comment_data = parser.parse_comment(html)

                                # 該貼文可能無人留言
                                if comment_data:
                                    # 將資料插入comments
                                    self.db_handler.insert_comment(comment_data)
                                self.back()
                    except Exception as e:
                        self.scraper_log.error(e)

                # 爬完一頁，等待<上頁元素載入
                is_load = self.wait_for_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]', 6)
                if is_load:
                    # 定位<上頁元素
                    find_old_bottom = self.find_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]')

                    # 點擊<上頁元素
                    self.click_element(find_old_bottom)


        except Exception as e:
            self.scraper_log.error(f"爬取過程中發生錯誤: {e}")
            time.sleep(20)
            return []

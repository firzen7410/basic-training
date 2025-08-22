from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import List, Dict, Any
from .base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ExampleScraper(BaseScraper):
    """範例爬蟲 - 爬取 Google 搜尋結果"""

    def __init__(self, driver, search_query: str = "Python Selenium"):
        super().__init__(driver)
        self.search_query = search_query
        self.base_url = "https://www.google.com"

    def scrape(self) -> List[Dict[str, Any]]:
        """主要爬蟲方法"""
        try:
            logger.info(f"開始爬取 Google 搜尋結果: {self.search_query}")

            # 導航到 Google
            if not self.navigate_to(self.base_url):
                return []

            # 等待搜尋框出現
            search_box = self.wait_for_element(By.NAME, "q")
            if not search_box:
                logger.error("找不到搜尋框")
                return []

            # 輸入搜尋關鍵字
            search_box.clear()
            search_box.send_keys(self.search_query)
            search_box.send_keys(Keys.RETURN)

            # 等待搜尋結果載入
            self.wait_for_element(By.ID, "search")

            # 爬取搜尋結果
            results = self._scrape_search_results()

            logger.info(f"成功爬取 {len(results)} 筆搜尋結果")
            return results

        except Exception as e:
            logger.error(f"爬取過程中發生錯誤: {e}")
            return []

    def _scrape_search_results(self) -> List[Dict[str, Any]]:
        """爬取搜尋結果"""
        results = []

        # 查找所有搜尋結果
        result_elements = self.find_elements_safe(By.CSS_SELECTOR, "div.g")

        for i, element in enumerate(result_elements[:10]):  # 只取前10個結果
            try:
                # 提取標題
                title_element = element.find_element(By.CSS_SELECTOR, "h3")
                title = title_element.text if title_element else "無標題"

                # 提取連結
                link_element = element.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href") if link_element else ""

                # 提取摘要
                snippet_element = element.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                snippet = snippet_element.text if snippet_element else "無摘要"

                result = {
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "rank": i + 1
                }

                results.append(result)
                logger.debug(f"爬取結果 {i + 1}: {title}")

            except Exception as e:
                logger.warning(f"處理搜尋結果 {i + 1} 時發生錯誤: {e}")
                continue

        return results

    def scrape_multiple_pages(self, num_pages: int = 3) -> List[Dict[str, Any]]:
        """爬取多頁搜尋結果"""
        all_results = []

        for page in range(num_pages):
            logger.info(f"爬取第 {page + 1} 頁")

            if page == 0:
                # 第一頁已經在 scrape() 方法中處理
                results = self._scrape_search_results()
            else:
                # 點擊下一頁
                next_button = self.find_element_safe(By.ID, "pnnext")
                if next_button and self.click_element(next_button):
                    self.add_delay(2)
                    results = self._scrape_search_results()
                else:
                    logger.info("沒有更多頁面")
                    break

            all_results.extend(results)

        return all_results
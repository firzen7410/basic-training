from selenium import webdriver
from scraper import Scraper
from database_handler import DatabaseHandler
from scraper_log_setup import set_scraper_log

# 拿到爬蟲用的log
scraper_log = set_scraper_log()

# 建立資料庫處理物件
db_handler = DatabaseHandler(scraper_log)
driver = webdriver.Chrome()

# 建立爬蟲物件並啟動
task = Scraper(driver, scraper_log, db_handler)
task.scrape_ptt('home-sale')

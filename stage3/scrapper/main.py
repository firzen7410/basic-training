import os
import dotenv
import logging
import pymysql
from selenium import webdriver
from scraper import Scraper
from database_handler import DatabaseHandler

# 建立log
scraper_log = logging.getLogger('selenium')
scraper_log.setLevel(logging.INFO)

# 建立console_header
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 建立file_handler
file_handler = logging.FileHandler("scraper_log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 設置formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
# 綁定header
scraper_log.addHandler(console_handler)
scraper_log.addHandler(file_handler)

dotenv.load_dotenv('config.env')

db_handler = DatabaseHandler(scraper_log)
driver = webdriver.Chrome()
task = Scraper(driver, scraper_log, db_handler)
task.scrape_ptt()

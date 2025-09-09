import os
import logging


def set_scraper_log():
    # 建立log
    scraper_log = logging.getLogger('selenium')
    scraper_log.setLevel(logging.INFO)

    # 建立console_header
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 建立file_handler
    log_path = os.path.join(os.path.dirname(__file__), "scraper_log")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # 設置formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    # 綁定header
    scraper_log.addHandler(console_handler)
    scraper_log.addHandler(file_handler)

    return scraper_log

from celery import Celery
from celery.schedules import crontab
from stage3.scrapper.scraper_log_setup import set_scraper_log
from stage3.scrapper.database_handler import DatabaseHandler
from stage3.scrapper.scraper import Scraper
from selenium import webdriver

# 建立 Celery app
app = Celery(
    "tasks",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379"
)

app.conf.timezone = "Asia/Taipei"
app.conf.enable_utc = False

app.conf.beat_schedule = {
    'scrape-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_gossiping',
        'schedule': crontab(minute=0),  # 每小時的整點執行
    },
}


@app.task(time_limit=3600, soft_time_limit=3540)
def scraper_gossiping():
    scraper_log = set_scraper_log()
    db_handler = DatabaseHandler(scraper_log)
    driver = webdriver.Chrome()
    try:
        task = Scraper(driver, scraper_log, db_handler)
        task.scrape_ptt()
    finally:
        driver.quit()

from celery import Celery
from celery.schedules import crontab
from stage3.scrapper.scraper_log_setup import set_scraper_log
from stage3.scrapper.database_handler import DatabaseHandler
from stage3.scrapper.scraper import Scraper
from selenium import webdriver

app = Celery(
    "tasks",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379"
)

app.conf.timezone = "Asia/Taipei"
app.conf.enable_utc = False

# beat 設定
app.conf.beat_schedule = {
    'scrape-gossiping-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_gossiping',
        'schedule': crontab(minute=0),
    },
    'scrape-stock-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_stock',
        'schedule': crontab(minute=10),
    },
    'scrape-japan_travel-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_life_is_money',
        'schedule': crontab(minute=20),
    },
    'scrape-PC_Shopping-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_pc_shopping',
        'schedule': crontab(minute=30),
    },
    'scrape-tech_job-every-hour': {
        'task': 'stage3.scrapper.celery_test.scraper_tech_job',
        'schedule': crontab(minute=40),
    },
}


def run_scraper(board):
    scraper_log = set_scraper_log()
    db_handler = DatabaseHandler(scraper_log)
    driver = webdriver.Chrome()
    task = Scraper(driver, scraper_log, db_handler)
    task.scrape_ptt(board)


@app.task()
def scraper_gossiping():
    run_scraper("Gossiping")


@app.task()
def scraper_stock():
    run_scraper("Stock")


@app.task()
def scraper_life_is_money():
    run_scraper("Lifeismoney")


@app.task()
def scraper_pc_shopping():
    run_scraper("PC_Shopping")


@app.task()
def scraper_tech_job():
    run_scraper("Tech_Job")

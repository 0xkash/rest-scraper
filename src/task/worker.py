from celery import Celery

from scrapers.schep_scraper import SchepScraper
from schema.scraper import Scraper

from utils.config import Config
from utils.logger import Logger

logger = Logger(__name__, "./logs/celery-worker-%Y-%m-%d.log")

celery = Celery(
    __name__, 
    broker=Config.get('CELERY_BROKER_URL'), 
    backend=Config.get('CELERY_RESULT_BACKEND')
)

celery.conf.imports = ('scrapers.schep_scraper',)

@celery.task(name='scraper_task')
def queue_scraper_task(scraper_dump):
    scraper_model: Scraper = Scraper(**scraper_dump)
    if scraper_model.id and scraper_model.scraper == "SchepScraper":
        scraper = SchepScraper(scraper_model.id, scraper_model.url, scraper_model.filters)
        scraper.run()
    
    return True
from typing import List
from fastapi import Depends
from datetime import datetime

from repository.scraper_repository import ScraperRepository
from schema.property import Property
from schema.scraper import Scraper
from scrapers.base_scraper import BaseScraper

from utils.logger import Logger

logger = Logger(__name__)

class ScraperService:
    def __init__(self, repository: ScraperRepository = Depends()) -> None:
        self.repository = repository

    def create(self, scraper: Scraper):
        return self.repository.create(scraper)

    def update(self, id: int, scraper: Scraper):
        return self.repository.update(id, scraper)
    
    def get(self, id: int):
        return self.repository.get(id)

    def scrape(self, scraper: BaseScraper):
        print("Scraping...")
        return scraper.scrape()
from typing import List
from fastapi import Depends
from datetime import datetime

from repository.scraper_repository import ScraperRepository
from schema.property import Property
from scrapers.base_scraper import BaseScraper

sample_data = {
    "name": "Sample Name 01",
    "description": "Just a general description of a property",
    "price": 735.00,
    "service_costs": 64.50,
    "address": "Sample Address 01",
    "city": "Sample City 01",
    "area": "65m²",
    "bedrooms": 2,
    "image": None,
}

class ScraperService:
    def __init__(self, repository: ScraperRepository = Depends()) -> None:
        self.repository = repository

    def scrape(self, scraper: BaseScraper):
        print("Scraping...")
        return scraper.scrape()
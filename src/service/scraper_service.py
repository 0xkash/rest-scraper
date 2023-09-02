from typing import List
from fastapi import Depends

from repository.scraper_repository import ScraperRepository
from schema.property import Property

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

    def scrape(self):
        print("Scraping...")
        return [
            {
                "name": "Sample Name 01",
                "description": "Just a general description of a property",
                "price": 974.00,
                "service_costs": 64.50,
                "address": "Sample Address 01",
                "city": "Sample City 01",
                "area": "89m²",
                "bedrooms": 2,
                "image": None,
            },
            {
                "name": "Sample Name 02",
                "description": "Just a general description of a property",
                "price": 735.00,
                "service_costs": 35.00,
                "address": "Sample Address 02",
                "city": "Sample City 02",
                "area": "55m²",
                "bedrooms": 1,
                "image": None,
            }
        ]
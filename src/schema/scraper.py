from typing import List
from datetime import datetime

from pydantic import BaseModel

class Scraper(BaseModel):
    id: int
    url: str | None = None
    scraper: str | None = None
    created_on: datetime
    updated_on: datetime | None = None
    deleted_on: datetime | None = None

class ScraperFilter(BaseModel):
    city: List[str]
    min_price: float | None = None
    max_price: float | None = None
    min_area: float | None = None
    max_area: float | None = None
    min_bedrooms: int | None = None
    max_bedrooms: int | None = None

class ScraperRequest(BaseModel):
    url: str | None = None
    scraper: str | None = None
    filter: ScraperFilter | None = None
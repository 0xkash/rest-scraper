from typing import List
from datetime import datetime

from pydantic import BaseModel

from .property import Property

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
    executed: bool | None = False
    filters: ScraperFilter | None = None

class Scraper(BaseModel):
    id: int | None = None
    url: str | None = None
    scraper: str | None = None
    filters: ScraperFilter | None = None
    state: str = "IDLE"
    task_id: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime | None = None
    deleted_on: datetime | None = None
    properties: list[Property] = []

    class Config:
        from_attributes = True
from datetime import datetime

from pydantic import BaseModel

class Property(BaseModel):
    id: int | None = None
    url: str
    address: str
    city: str
    price: float
    area: int | float
    available_on: str | None = None
    rooms: int | None = None
    description: str | None = None
    meta_data: dict[str, str] | None = None
    images: list[str] | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime | None = None
    scraper_id: int

    class Config:
        from_attributes = True
from typing import List
from datetime import datetime

from pydantic import BaseModel

class Property(BaseModel):
    url: str
    address: str
    description: str
    city: str
    price: float
    service_costs: float
    area: str
    bedrooms: int | None = None
    images: List[str] | None = None
    created_on: datetime
    updated_on: datetime | None = None
    deleted_on: datetime | None = None
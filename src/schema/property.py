from pydantic import BaseModel

class Property(BaseModel):
    name: str
    description: str
    price: float
    service_costs: float
    address: str
    city: str
    area: str
    bedrooms: int | None = None
    image: str | None = None
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    pass

from .property_model import PropertyModel
from .scraper_model import ScraperModel
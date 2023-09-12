from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from schema.pyandic_type import PydanticType
from schema.scraper import ScraperFilter

from model import BaseModel

class ScraperModel(BaseModel):
    __tablename__ = 'scrapers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    scraper = Column(String, nullable=True)
    filters = Column(PydanticType(ScraperFilter), nullable=True)
    state = Column(String, nullable=False)
    task_id = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.now())
    updated_on = Column(DateTime, onupdate=datetime.now(), nullable=True)

    properties = relationship('PropertyModel', back_populates='scraper')
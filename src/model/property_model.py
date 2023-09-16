from sqlalchemy import ForeignKey, Numeric, Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType
from datetime import datetime

from model import BaseModel

class PropertyModel(BaseModel):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    area = Column(Numeric, nullable=False)
    available_on = Column(String, nullable=True)
    rooms = Column(Numeric, nullable=True)
    description = Column(Text, nullable=True)
    meta_data = Column(JSONType, nullable=True)
    images = Column(ARRAY(String), nullable=True, default=list())
    created_on = Column(DateTime, nullable=False, default=datetime.now())
    updated_on = Column(DateTime, nullable=True, onupdate=datetime.now())
    scraper_id = Column(Integer, ForeignKey('scrapers.id'))

    scraper = relationship('ScraperModel', back_populates='properties')
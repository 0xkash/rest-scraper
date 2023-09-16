from fastapi import Depends
from sqlalchemy.orm import Session

from schema.property import Property
from model.property_model import PropertyModel

from utils.database import Database

class PropertyRepository:
    def __init__(self, db_session: Session = Depends(Database.get_session)) -> None:
        self.db = db_session

    def create(self, property: Property) -> PropertyModel:
        property_model = PropertyModel(
                url=property.url,
                address=property.address,
                city=property.city,
                price=property.price,
                area=property.area,
                available_on=property.available_on,
                rooms=property.rooms,
                description=property.description,
                meta_data=property.meta_data,
                images=property.images,
                scraper_id=property.scraper_id,
            )
        self.db.add(property_model)
        self.db.commit()
        
        return property_model
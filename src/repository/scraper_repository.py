from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import json

from schema.scraper import Scraper
from model.scraper_model import ScraperModel

from utils.database import Database

class ScraperRepository:
    def __init__(self, db_session: Session = Depends(Database.get_session)) -> None:
        self.db = db_session

    def create(self, scraper: Scraper):
        db_scraper = ScraperModel(
                state=scraper.state,
                url=scraper.url,
                scraper=scraper.scraper,
                filters=scraper.filters,
            )
        self.db.add(db_scraper)
        self.db.commit()
        self.db.refresh(db_scraper)

        return db_scraper
    
    def update(self, id: int, scraper: Scraper):
        db_scraper = self.get(id)
        scraper_object = scraper.model_dump(exclude_unset=True)

        for key, value in scraper_object.items():
            setattr(db_scraper, key, value)
    
        self.db.add(db_scraper)
        self.db.commit()
        self.db.refresh(db_scraper)

        return db_scraper
    
    def get(self, id: int):
        db_scraper = self.db.query(ScraperModel).filter(ScraperModel.id == id).first()
        if not db_scraper:
            raise HTTPException(status_code=404, detail="Scraper not found")
        return db_scraper
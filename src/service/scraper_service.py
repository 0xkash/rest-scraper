from fastapi import Depends, HTTPException

from repository.scraper_repository import ScraperRepository
from schema.scraper import Scraper

from task.worker import queue_scraper_task

from utils.logger import Logger

logger = Logger(__name__)

class ScraperService:
    def __init__(self, repository: ScraperRepository = Depends()) -> None:
        self.repository = repository

    def create(self, scraper: Scraper):
        return self.repository.create(scraper)

    def update(self, id: int, scraper: Scraper):
        return self.repository.update(id, scraper)
    
    def get(self, id: int):
        scraper: Scraper = Scraper.model_validate(self.repository.get(id))
        if scraper.task_id and scraper.state is not "IDLE":
            scraper.state = queue_scraper_task.AsyncResult(scraper.task_id).state
        return scraper
    
    def run(self, id: int):
        scraper: Scraper = Scraper.model_validate(self.repository.get(id))
        if scraper is None:
            return False
        
        if not scraper.url and not scraper.scraper:
            raise HTTPException(status_code=400, detail="Scraper has no url or scraper")
        if not scraper.filters:
            raise HTTPException(status_code=400, detail="Scraper has no filters")
        
        if scraper.scraper:
            task = queue_scraper_task.delay(scraper.model_dump())
            scraper.state = task.state
            scraper.task_id = task.task_id
            self.repository.update(id, scraper)
            return task.task_id
        elif scraper.url:
            # TODO: Implement BaseScraper url scraper
            raise HTTPException(status_code=404, detail="Base URL Scraper not implemented")
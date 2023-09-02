from fastapi import APIRouter, status, Depends
from typing import List

from fastapi.responses import JSONResponse
from fastapi_router_controller import Controller

from service.scraper_service import ScraperService
from schema.property import Property

router = APIRouter(prefix="/scraper")

controller = Controller(router, {
    "name": "scraper",
    "description": "This API is responsible for scraping operations",
})

@controller.use()
@controller.resource()
class ScraperController:
    def __init__(self, service: ScraperService = Depends()) -> None:
        self.service = service

    @controller.router.get(
        "",
        tags=["scraper"], 
        summary="Add new scraper action to the queue based on the given parameters", 
        response_model=List[Property],
        status_code=status.HTTP_200_OK
    )
    def scrape(self):
        return self.service.scrape()
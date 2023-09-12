from validators import url as url_validator

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_router_controller import Controller

from service.scraper_service import ScraperService
from schema.scraper import ScraperRequest
from schema.scraper import Scraper

router = APIRouter(prefix="/scraper")

controller = Controller(router, {
    "name": "scraper",
    "description": "This API is responsible for scraping operations",
})

scraper_urls = {
    "SchepScraper": "https://schepvastgoedmanagers.nl",
}

@controller.use()
@controller.resource()
class ScraperController:
    def __init__(self, service: ScraperService = Depends()) -> None:
        self.service = service

    @controller.router.post(
        "",
        tags=["scraper"], 
        summary="Add new scraper action to the queue based on the given parameters", 
        response_model=Scraper,
        status_code=status.HTTP_200_OK
    )
    def create(self, request: ScraperRequest):
        # Either only url or only scraper must be provided
        if (not request.url and not request.scraper) or (request.url and request.scraper):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Either url or scraper must be provided"}
            )
        
        scraper = Scraper(filters=request.filters)
        if request.scraper and request.scraper in scraper_urls:
            scraper.url = scraper_urls[request.scraper]
            scraper.scraper = request.scraper
        elif request.url and url_validator(request.url):
            scraper.url = request.url
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "No valid url or scraper was provided"}
            )
        
        return self.service.create(scraper)
    
    @controller.router.put(
        "/{id}",
        tags=["scraper"], 
        summary="Update scraper by id", 
        response_model=Scraper,
        status_code=status.HTTP_200_OK
    )
    def update(self, id: int, request: ScraperRequest):
        return self.service.update(id, Scraper(**request.model_dump()))
    
    @controller.router.get(
        "/{id}",
        tags=["scraper"], 
        summary="Get scraper by id", 
        response_model=Scraper,
        status_code=status.HTTP_200_OK
    )
    def get(self, id: int):
        return self.service.get(id)
    
    # TODO: Execute scrapers if they are not executed yet
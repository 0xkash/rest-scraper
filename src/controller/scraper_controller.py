from typing import List
from validators import url as url_validator

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_router_controller import Controller

from service.scraper_service import ScraperService
from schema.property import Property
from schema.scraper import ScraperRequest

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

    @controller.router.post(
        "",
        tags=["scraper"], 
        summary="Add new scraper action to the queue based on the given parameters", 
        response_model=dict[str, str],
        status_code=status.HTTP_200_OK
    )
    def scrape(self, request: ScraperRequest):
        # Either only url or only scraper must be provided
        if (not request.url and not request.scraper) or (request.url and request.scraper):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Either url or scraper must be provided"}
            )
        
        from scrapers.base_scraper import BaseScraper
        scraper = BaseScraper()

        if request.url and url_validator(request.url):
            # TODO: Use base scraper to scrape the given url
            pass

        if request.scraper:
            if request.scraper == "schep":
                from scrapers.schep_scraper import SchepScraper
                scraper = SchepScraper(request.filter)
        
        # TODO: If its a scraper, check if scraper class exists
        return self.service.scrape(scraper)
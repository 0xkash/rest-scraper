from selenium import webdriver
from selenium.webdriver import FirefoxOptions

from schema.scraper import ScraperFilter

class BaseScraper:
    def __init__(self, id: int, url: str | None = None, filters: ScraperFilter | None = None):
        self.id = id
        self.url = url
        self.filters = filters

        self.driver = None

    def set_url(self, url: str):
        self.url = url

    def set_filters(self, filters: ScraperFilter):
        self.filters = filters

    def init_driver(self):
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options)

    def run(self):
        # TODO: Implement this method
        pass
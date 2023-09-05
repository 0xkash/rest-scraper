from schema.scraper import ScraperFilter

class BaseScraper:
    def __init__(self, url: str | None = None, filters: ScraperFilter | None = None):
        self.url = url
        self.filters = filters

    def set_url(self, url: str):
        self.url = url

    def set_filters(self, filters: ScraperFilter):
        self.filters = filters

    def scrape(self):
        # TODO: Implement this method
        pass
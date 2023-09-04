import traceback

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import requests
from bs4 import BeautifulSoup

from schema.scraper import ScraperFilter
from scrapers.base_scraper import BaseScraper

from utils.logger import Logger

logger = Logger(__name__, "./logs/schep-scraper-%Y-%m-%d.log")

class SchepScraper(BaseScraper):
    def __init__(self, filters: ScraperFilter | None = None):
        self.BASE_URL = "https://schepvastgoedmanagers.nl/Verhuur/"
        # The minimal filter price
        self.MIN_PRICE = 0
        # The maximal filter price
        self.MAX_PRICE = 1250
        self.selected_addresses: dict[str, str] = {}
        self.filters = filters

        options = FirefoxOptions()
        options.add_argument("--headless")

        self.driver = webdriver.Firefox(options)
        self.driver.maximize_window()

    def select_city(self, city: str) -> None:
        city_select_element = self.driver.find_element(By.CSS_SELECTOR, "#Main_ctl00_ctl03")
        city_options = city_select_element.find_elements(By.TAG_NAME, "option")
        is_selected = False
        cities = list(map(lambda city_option: city_option.get_attribute("value"), city_options))
        for city_value in cities:
            # A fix when DOM changes select option
            city_option = self.driver.find_element(By.CSS_SELECTOR, f"option[value='{city_value}']")
            if not city_option.get_attribute("value"):
                continue
            if city_option.get_attribute("value") == city:
                is_selected = True
                city_option.click()
                if self.filters and (self.filters.min_price or self.filters.max_price):
                    self.select_price_range(self.filters.min_price, self.filters.max_price)

        if not is_selected:
            raise Exception(f"City {city} was not found in selection!")
    
    def select_price_range(self, min_price, max_price) -> None:
        min_price = int(min_price or self.MIN_PRICE)
        max_price = int(max_price or self.MAX_PRICE + 1)
        price_select_element = self.driver.find_element(By.CSS_SELECTOR, "#Main_ctl00_ctl11")
        price_options = price_select_element.find_elements(By.TAG_NAME, "option")
        if len(price_options) > 1:
            prices = list(map(lambda price_option: price_option.get_attribute("value"), price_options))
            for price in prices:
                # A fix when DOM changes select option
                price_option = self.driver.find_element(By.CSS_SELECTOR, f"option[value='{price}']")
                if not price:
                    continue

                price_range = str(price).split(",")
                selected_min_price = int(price_range[0] or self.MIN_PRICE)
                selected_max_price = int(price_range[1] or self.MAX_PRICE + 1)
                
                if selected_min_price >= min_price and selected_max_price <= max_price:
                    price_option.click()
                    self.get_available_addresses(str(price))
        else:
            raise Exception(f"Price range {min_price}-{max_price} was not found in selection!")
    
    def get_available_addresses(self, price_range: str) -> None:
        address_select_element = self.driver.find_element(By.CSS_SELECTOR, "#Main_ctl00_ctl05")
        address_options = address_select_element.find_elements(By.TAG_NAME, "option")
        if (len(address_options) > 1):
            for address_option in address_options:
                if not address_option.get_attribute("value"):
                    continue

                self.selected_addresses.update({
                    str(address_option.get_attribute("value")): price_range
                })

    def scrape_addresses(self) -> None:
        if self.filters:
            # Filter cities if available
            if self.filters.city and len(self.filters.city) > 0:
                for city in self.filters.city:
                    self.select_city(city)


    def scrape(self) -> dict[str, str]:
        self.driver.get(self.BASE_URL)
        # Check for cookie wall and accept it
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "ctl17_GiveFullConsent")))
            self.driver.find_element(By.ID, "ctl17_GiveFullConsent").click()
        except Exception as e:
            logger.info(f"Cookie wall was not found for: {self.BASE_URL} - {e}")
        
        try:
            self.scrape_addresses()
        except Exception as e:
            logger.error(f"Could not scrape with given: {e}")
            logger.error(traceback.format_exc())
        #soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.driver.close()
        return self.selected_addresses
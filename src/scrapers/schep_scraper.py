import traceback
from typing import List

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from schema.scraper import ScraperFilter
from schema.property import Property
from scrapers.base_scraper import BaseScraper
from mapper.property_mapper import PropertyMapper

from utils.logger import Logger

logger = Logger(__name__, "./logs/schep-scraper-%Y-%m-%d.log")

# TODO: Rewrite this class (This might be faster and less cpu intensive)
    # TODO: Scrape based on selected city
    # TODO: Scrape every found address and map it to a property object
    # TODO: Check for filters and compare it to the property
    # TODO: Automatic pagination until the end of the page

class SchepScraper(BaseScraper):
    def __init__(self, filters: ScraperFilter | None = None):
        self.BASE_URL = "https://schepvastgoedmanagers.nl"
        self.filters = filters
        self.selected_addresses: dict[str, str] = {}

        options = FirefoxOptions()
        options.add_argument("--headless")

        self.driver = webdriver.Firefox(options)

    def select_city(self, city: str) -> bool:
        # TODO: Dynamically select CSS selector (should be available as front end)
        city_select_element = self.driver.find_element(By.CSS_SELECTOR, "#Main_ctl00_ctl03")
        city_options = city_select_element.find_elements(By.TAG_NAME, "option")
        # Map all cities to string
        cities = list(map(lambda city_option: city_option.get_attribute("value"), city_options))
        for city_value in cities:
            # A fix when DOM changes select option
            city_option = self.driver.find_element(By.CSS_SELECTOR, f"option[value='{city_value}']")
            if not city_option.get_attribute("value"):
                continue

            if city_option.get_attribute("value") == city:
                city_option.click()
                return True
            
        return False
    
    def get_property_selection(self) -> List[Property]:
        properties: List[Property] = []

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".woningList")))
        # TODO: Dynamically select CSS selector (should be available as front end)
        property_objects = self.driver.find_element(By.CSS_SELECTOR, ".woningList")
        properties_element = property_objects.find_elements(By.CSS_SELECTOR, ".object")

        for property_element in properties_element:
            url = f"{str(property_element.get_attribute('href'))}"
            bs = BeautifulSoup(str(property_element.get_attribute("innerHTML")), "html.parser")
            info_element = bs.find(class_="extrainfo") # type: ignore
            price = info_element.find(class_="waarde").find(class_="prijs").get_text() # type: ignore
            parsed_price = PropertyMapper.parse_price(price)
            
            # Check for price filters if they exist
            if self.filters and (self.filters.min_price or self.filters.max_price):
                if self.filters.min_price and parsed_price < self.filters.min_price:
                    continue
                if self.filters.max_price and parsed_price > self.filters.max_price:
                    continue
            
            # Gather all relevant property information
            address = bs.find(class_="straat").get_text() # type: ignore
            city = bs.find(class_="plaats").get_text() # type: ignore
            area = info_element.find(lambda tag:tag.name=="div" and "Woonoppervlak" in tag.text).get_text() # type: ignore
            image = f"{self.BASE_URL}{bs.find(class_='hoofdfotocontainer').find('img').attrs['src']}" # type: ignore
            room_element = info_element.find(lambda tag:tag.name=="div" and "Kamers" in tag.text) # type: ignore
            rooms = room_element.get_text() if room_element else None # type: ignore
            available = info_element.find(class_="Beschikbaar").find("span").get_text() # type: ignore
            
            # Map to propety object
            property = PropertyMapper({
                "url": url,
                "address": address, # Remove leading whitespace
                "city": city,
                "price": price,
                "area": area,
                "available_on": available,
                "rooms": rooms,
                "images": image
            }).map()
            properties.append(property)
            
        return properties

    def scrape(self) -> List[Property]:
        properties: List[Property] = []
        self.driver.get(f"{self.BASE_URL}/Verhuur")
        # Check for cookie wall and accept it
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "ctl17_GiveFullConsent")))
            self.driver.find_element(By.ID, "ctl17_GiveFullConsent").click()
        except Exception as e:
            logger.info(f"Cookie wall was not found for: {self.BASE_URL} - {e}")

        if self.filters and self.filters.city:
            for city in self.filters.city:
                self.driver.get(f"{self.BASE_URL}/Verhuur")
                try:
                    if self.select_city(city):
                        # Simulate search button click
                        # TODO: Dynamically select CSS selector (should be available as front end)
                        self.driver.find_element(By.CSS_SELECTOR, "#Main_ctl00_WoningZoekButton").click()
                        properties.extend(self.get_property_selection())
                    else:
                        logger.error(f"City: {city} was not found for: {self.BASE_URL}")
                except Exception as e:
                    logger.error(f"Exception when scraping - {e}")
                    logger.error(traceback.format_exc())
        else:
            logger.error(f"No filters were found for: {self.BASE_URL}")
        
        self.driver.close()
        return properties
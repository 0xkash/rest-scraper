from typing import Any, List

from schema.property import Property

class PropertyMapper:
    def __init__(self, attributes: dict[str, Any]):
        self.attributes = attributes

    @staticmethod
    def parse_price(price: str) -> float:
        # This maybe to specific, maybe change in the future
        return float(price
                     .replace("Huurprijs:", "")
                     .replace("€ ", "")
                     .replace(".", "")
                     .replace(",", ".")
                     .replace("-", "")
                     .replace("p/m", ""))
    
    @staticmethod
    def parse_rooms(rooms: str) -> int | None:
        return int(rooms.replace("Kamers:", "")) if rooms else None
    
    @staticmethod
    def parse_area(area: str) -> str:
        return area.replace("Woonoppervlak:", "").lstrip() # remove nbsp
    
    @staticmethod
    def parse_images(images: str) -> List[str]:
        return images if type(images) is List else [images]

    def map(self) -> Property:
        property: dict = {}

        for attribute in self.attributes.keys():
            if attribute == "price":
                property[attribute] = self.parse_price(self.attributes[attribute])
            elif attribute == "rooms":
                property[attribute] = self.parse_rooms(self.attributes[attribute])
            elif attribute == "area":
                property[attribute] = self.parse_area(self.attributes[attribute])
            elif attribute == "images":
                property[attribute] = self.parse_images(self.attributes[attribute])
            else:
                property[attribute] = self.attributes[attribute].lstrip()

        return Property(**property)
    
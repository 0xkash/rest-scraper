from fastapi import Depends, HTTPException

from repository.property_repository import PropertyRepository

from utils.logger import Logger

logger = Logger(__name__)

class PropertyService:
    def __init__(self, repository: PropertyRepository = Depends()) -> None:
        self.repository = repository

    def get(self, id: int):
        return self.repository.get(id)

    def list(self):
        return self.repository.list()
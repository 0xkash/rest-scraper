from fastapi import APIRouter, status, Depends
from fastapi_router_controller import Controller

from service.property_service import PropertyService
from schema.property import Property

router = APIRouter(prefix="/property")

controller = Controller(router, {
    "name": "property",
    "description": "This API is responsible for property operations",
})

@controller.use()
@controller.resource()
class PropertyController:
    def __init__(self, service: PropertyService = Depends()) -> None:
        self.service = service

    @controller.router.get(
        "/{id}",
        tags=["property"], 
        summary="Get property by id", 
        response_model=Property,
        status_code=status.HTTP_200_OK
    )
    def get(self, id: int):
        return self.service.get(id)
    
    @controller.router.get(
        "",
        tags=["property"], 
        summary="List all properties", 
        response_model=list[Property],
        status_code=status.HTTP_200_OK
    )
    def list(self):
        return self.service.list()
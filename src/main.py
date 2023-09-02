from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from fastapi_router_controller import Controller, ControllersTags

import debugpy

from utils.config import Config
from utils.middleware import ExceptionHandler, RequestHandler
# Import all controllers
import controller

debugpy.listen(5678)

app = FastAPI(
    title=Config.get("APP_NAME"),
    description=Config.get("APP_DESCRIPTION"),
    version=Config.get("APP_VERSION"),
    debug=Config.get("ENVIRONMENT") == "development",
    redoc_url=Config.get("DOCS_PATH"),
    openapi_tags=ControllersTags
)

# Handle all exceptions and validation errors
app.exception_handler(Exception)(ExceptionHandler.handle)
app.exception_handler(RequestValidationError)(ExceptionHandler.handle)
# Handle all requests
app.add_middleware(RequestHandler)

# Load all controller routes
for router in Controller.routers():
    app.include_router(router)
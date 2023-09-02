from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import debugpy

from .utils.config import Config
from .utils.middleware import ExceptionHandler, RequestHandler

debugpy.listen(5678)

app = FastAPI(
    title=Config.get("APP_NAME"),
    description=Config.get("APP_DESCRIPTION"),
    version=Config.get("APP_VERSION"),
    debug=Config.get("ENVIRONMENT") == "development",
    redoc_url=Config.get("DOCS_PATH"),
)

# Handle all exceptions and validation errors
app.exception_handler(Exception)(ExceptionHandler.handle)
app.exception_handler(RequestValidationError)(ExceptionHandler.handle)
# Handle all requests
app.add_middleware(RequestHandler)


@app.get("/")
def read_root():
    return {
        "App Name": Config.get("APP_NAME"),
        "Current environment": Config.get("ENVIRONMENT"),
    }
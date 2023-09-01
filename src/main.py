from fastapi import FastAPI
import debugpy
from .utils.config import Config

debugpy.listen(5678)

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "App Name": Config.get("APP_NAME"),
        "Current environment": Config.get("ENVIRONMENT"),
    }
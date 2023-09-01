from fastapi import FastAPI
import debugpy

debugpy.listen(5678)
debugpy.wait_for_client()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "3333"}
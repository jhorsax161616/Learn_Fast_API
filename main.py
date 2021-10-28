from typing import Dict
from fastapi import FastAPI
from typing import Dict

app: FastAPI = FastAPI()

@app.get("/")   
def home() -> Dict:
    return {"Hello": "World!!"}
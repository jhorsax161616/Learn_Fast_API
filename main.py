#Python
from typing import Dict
from typing import Optional
from fastapi.param_functions import Query

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query


app: FastAPI = FastAPI()

#Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None #Para poder asignar que la variable es opcional[tipo]
    is_married: Optional[bool] = None # Se le pone None para q' cuando no se le pase algo le asigne NULL(BaseDatos)

    
@app.get("/")   
def home() -> Dict:
    return {"Hello": "World!!"}


#Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)): # Body(...) los 3 puntos son para asignar que el parámetro es obligatorio
    return person

#Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=2, max_length=50), #Los query parameters son opcionales y usammos min y max para restringir la entrada
    age: str = Query(...)
):
    return {name: age}
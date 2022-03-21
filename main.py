#Python
from operator import gt
from typing import Dict
from typing import Optional
from fastapi.param_functions import Query
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import NegativeFloat

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path


app: FastAPI = FastAPI()

#Models

##Modelo para validar el haircolor
class HairColor(Enum):
    white: str = "white"
    black: str = "black"
    brown: str = "brown"
    blonde: str = "blonde"
    red: str = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30)
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30)
    age: int = Field(
        ...,
        gt=0,
        le=95
    )
    hair_color: Optional[HairColor] = Field(default=None) #Para poder asignar que la variable es opcional[tipo]
    is_married: Optional[bool] = Field(default=None) # Se le pone None para q' cuando no se le pase algo le asigne NULL(BaseDatos)
    website: Optional[HttpUrl] = Field(default=None)
    number_negative: Optional[NegativeFloat]
    
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
    name: Optional[str] = Query(
        None,
        min_length=2,
        max_length=50,
        title = "Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ), #Los query parameters son opcionales y usammos min y max para restringir la entrada
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
):
    return {name: age}

#Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
         gt=0,
         title="Person Id",
         description="This is the person id. It's greater than 0"
         )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    #Debemos fusionar como diccionarios para recibir un json con todas las respuestas
    results = person.dict()
    results.update(location.dict())

    return results
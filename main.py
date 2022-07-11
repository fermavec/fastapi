#Python
from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from typing import Optional
from enum import Enum
#Pydantic!
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl
#Fast API
from fastapi import FastAPI
from fastapi import Body 
from fastapi import Query, Path


#Creando variable de ejecucion con instancia de la clase FastAPI
app = FastAPI()


#Models (Heredan de Base Model)
class HairColor(Enum):
    white = "White"
    black = "Black"
    brown = "Brown"
    blonde = "Blonde"
    red = "Red"


class Person(BaseModel):
    #Con tipado estatico
    #Con Field de pydantic haremos el validation model
    first_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50
    )
    last_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50
    )
    age: int = Field(
        ...,
        gt= 0,
        le= 115
    )
    email: EmailStr = Field(...)
    webpage: HttpUrl = Field(...)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Fernando",
                "last_name": "Mavec",
                "age": 35,
                "email": "fer@fermavec.com",
                "webpage": "http://www.fermavec.com",
                "hair_color": "Black",
                "is_married": False
            }
        }


class Location(BaseModel):
    country: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example = "MX"
    )
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example = "CDMX"
    )
    zip_code: str = Field(
        ...,
        min_length=4,
        max_length=5,
        example= "01020"
    )


#Path operation decorator para ejecución en el home ("/"")
@app.get("/")
def home():
    #Retorna un Json
    return {"Fernando": "Mavec"}


#Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):#Request Body, los ... significan parametro obligartorio
    return person


#Validations: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title= "Person Name",
        description="This is the person name. It's between 1 to 50 characters"
        ),
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It's required"
        )
):
    return {name: age}


#Validaciones: Path Parameters
@app.get("/person/details/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title= "Person ID",
        description= "This is the person id. It's required"
        )
):
    return {person_id: "it exists!"}


#Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the Person ID. It's Required",
        gt= 0
    ),
    person: Person = Body(
        ...
    ),
    location: Location = Body(
        ...
    )
):
    results = person.dict()
    results.update(location.dict())
    return results
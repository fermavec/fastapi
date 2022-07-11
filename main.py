#Python
from email.utils import decode_rfc2231
from typing import Optional
#Pydantic!
from pydantic import BaseModel
#Fast API
from fastapi import FastAPI
from fastapi import Body 
from fastapi import Query, Path


#Creando variable de ejecucion con instancia de la clase FastAPI
app = FastAPI()


#Models (Heredan de Base Model)
class Person(BaseModel):
    #Con tipado estatico
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


class Location(BaseModel):
    country: str
    city: str
    zip_code: int


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
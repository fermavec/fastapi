#Python
from typing import Optional
#Pydantic!
from pydantic import BaseModel
#Fast API
from fastapi import FastAPI
from fastapi import Body 


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


#Path operation decorator para ejecución en el home ("/"")
@app.get("/")
def home():
    #Retorna un Json
    return {"Fernando": "Mavec"}


#Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):#Request Body, los ... significan parametro obligartorio
    return person
#Python
from typing import Optional
from enum import Enum
#Pydantic!
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl
#Fast API
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException 
from fastapi import Body 
from fastapi import Query, Path, Form, Header, Cookie, UploadFile, File


#Creando variable de ejecucion con instancia de la clase FastAPI
app = FastAPI()


#Models (Heredan de Base Model)
class HairColor(Enum):
    white = "White"
    black = "Black"
    brown = "Brown"
    blonde = "Blonde"
    red = "Red"


class PersonBase(BaseModel):
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
                "is_married": False,
                "password": "HolasoyFer"
            }
        }


class Person(PersonBase):
    password: str = Field(
        ..., 
        min_length=8
        )

    
class PersonOut(PersonBase):
    pass


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


class LoginOut(BaseModel):
    username: str= Field(
        ...,
        max_Length=20,
        example="fermavec"
    )
    message: str = Field(default="Login Succesfully!")


#Path operation decorator para ejecución en el home ("/"")
@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags= ["Home"]
    )
def home():
    #Retorna un Json
    return {"Fernando": "Mavec"}


#Request and Response Body
@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags= ["Persons"]
    )
def create_person(person: Person = Body(...)):#Request Body, los ... significan parametro obligartorio
    return person


#Validations: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags= ["Persons"]
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title= "Person Name",
        description="This is the person name. It's between 1 to 50 characters",
        example= "Fer"
        ),
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the person age. It's required",
        example=35
        )
):
    return {name: age}


#Validaciones: Path Parameters
#HTTPException
persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/details/{person_id}",
    status_code=status.HTTP_200_OK,
    tags= ["Persons"]
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title= "Person ID",
        description= "This is the person id. It's required",
        example= 1
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist!"
        )
    else:
        return {person_id: "it exists!"}


#Validaciones: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags= ["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        description= "This is the Person ID. It's Required",
        gt= 0,
        example=1
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


#Working with forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags= ["Persons"]
    )
def login(
    username: str= Form(...), 
    password: str= Form(...) 
    ):
    return LoginOut(username=username)


#Coockies and Headers Parameters
@app.post(
    path= '/contact',
    status_code=status.HTTP_200_OK,
    tags= ["Contact"]
    )
def contact(
    first_name: str= Form(
        ...,
        max_Length=20,
        min_Length=1
        ),
    last_name: str= Form(
        ...,
        max_Length=20,
        min_Length=1
        ),
    email: EmailStr= Form(...),
    message: str= Form(
        ...,
        min_Length=20
        ),
    #header
    user_agent: Optional[str] = Header(default=None),
    #Cookie
    ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent


#Files
@app.post(
    path="/post-image",
    tags= ["Uploads"]
    )
def post_image(
    image: UploadFile = File()
    ):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
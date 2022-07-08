from fastapi import FastAPI

#Creando variable de ejecucion con instancia de la clase FastAPI
app = FastAPI()

#Path operation decorator para ejecución en el home ("/"")
@app.get("/")
def home():
    #Retorna un Json
    return {"Fernando": "Mavec"}


#Request and Response Body
@app.post("/person/new")
def create_person():
    pass
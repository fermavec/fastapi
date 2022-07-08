from fastapi import FastAPI

#Creando variable de ejecucion con instancia de la clase FastAPI
app = FastAPI()

#Path operation decorator para ejecución en el home ("/"")
@app.get("/")
def home():
    #Retorna un Json
    return {"Fernando": "Mavec"}
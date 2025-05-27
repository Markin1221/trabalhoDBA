from fastapi import FastAPI
from MongoDB import run       
from zobd import App
from dataWerehouse import main


run = FastAPI(title="API Integrada: MongoDB + PostgreSQL + ZODB")

# --- MongoDB ---
@run.get("/mongo")
def pegar_comentarios_mongo():
    return {"usuarios": run.escolherProduto()}

# --- PostgreSQL (Data Warehouse) ---
@run.get("/menu")
def menu():
    return {"menuOlap": main.menu()}

@run.get("/olap")
def olap():
    return {"Olap": main.mostrar_olap()}

# --- ZODB ---
@run.get("/zodb")
def menuzodb():
    return App.menu()

@run.get("/zodb/categorias")
def obter_categoria_existente():
    return App.obter_categoria_existente()
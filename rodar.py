from fastapi import FastAPI
from app import escolherProduto
from postgres_handler import listar_usuarios_postgres
from zodb_handler import pegar_pessoa_zodb

app = FastAPI()

@app.get("/mongo")
def get_mongo():
    return {"usuarios": listar_usuarios_mongo()}

@app.get("/postgres")
def get_postgres():
    return {"usuarios": listar_usuarios_postgres()}

@app.get("/zodb")
def get_zodb():
    return pegar_pessoa_zodb()
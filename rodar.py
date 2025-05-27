from fastapi import FastAPI
from MongoDB import run as mongo_run
from zobd.App import menu,obter_categoria_existente
from dataWerehouse import main,postegres
from zobd import BD

app = FastAPI(title="API Integrada: MongoDB + PostgreSQL + ZODB")

# --- MongoDB ---
@app.get("/mongo")
def pegar_comentarios_mongo():
    # Chama a função do MongoDB corretamente
    return {"usuarios": mongo_run.escolherProduto()}

# --- PostgreSQL (Data Warehouse) ---
# --- PostgreSQL ---
@app.get("/postgres/print")
def print_postgres():
    return {"print": postegres.listar_produtos_postgres()}

# --- ZODB ---
@app.get("/zodb/print")
def print_zodb():
    return {"printzo": BD.listar_produtos()}

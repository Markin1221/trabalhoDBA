from fastapi import FastAPI
from MongoDB import run       
from zobd import BD                   
from dataWerehouse import fetch_vendas_por_hora, fetch_olap_vendas_completo, get_dados_para_previsao 

run = FastAPI(title="API Integrada: MongoDB + PostgreSQL + ZODB")

# --- MongoDB ---
@run.get("/mongo")
def pegar_comentarios_mogo():
    return {"usuarios": run.escolherProduto()}

# --- PostgreSQL (Data Warehouse) ---
@run.get("/vendas/hora")
def vendas_por_hora():
    return fetch_vendas_por_hora()

@run.get("/olap")
def olap():
    return fetch_olap_vendas_completo()

@run.get("/previsao/dados")
def dados_previsao():
    return get_dados_para_previsao()

# --- ZODB ---
@run.get("/zodb")
def pegar_objeto_zodb():
    return ()
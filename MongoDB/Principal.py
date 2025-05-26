
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import mplcursors
import json

# --- Conexão MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["sistema_varejo"]
colecao_avaliacoes = db["avaliacoes"]

def adicionar_avaliacao(cliente_id, produto_id, nota, comentario, data=None):
    avaliacao = {
        "cliente_id": str(cliente_id),
        "produto_id": str(produto_id),
        "nota": nota,
        "comentario": comentario,
        "data": data or datetime.now()
    }
    resultado = colecao_avaliacoes.insert_one(avaliacao)
    print(f"Avaliação adicionada com ID: {resultado.inserted_id}")

def listar_avaliacoes_produto(produto_id):
    produto_id = str(produto_id)
    avaliacoes = list(colecao_avaliacoes.find({"produto_id": produto_id}))

    if not avaliacoes:
        print(f"Produto {produto_id} não possui avaliação.")
        return

    for a in avaliacoes:
        print(f"[{a['data'].strftime('%d/%m/%Y %H:%M:%S')}] Cliente {a['cliente_id']} - Nota: {a['nota']} - {a['comentario']}")

def remover_duplicatas():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "cliente_id": "$cliente_id",
                    "produto_id": "$produto_id",
                    "comentario": "$comentario",
                    "nota": "$nota"
                },
                "ids": {"$addToSet": "$_id"},
                "count": {"$sum": 1}
            }
        },
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicatas = list(colecao_avaliacoes.aggregate(pipeline))
    for doc in duplicatas:
        ids = doc["ids"]
        ids.pop(0)  # Mantém o primeiro
        colecao_avaliacoes.delete_many({"_id": {"$in": ids}})
        
def agrupar_clientes_por_comportamento(n_clusters=3):
    pipeline = [
        {
            "$group": {
                "_id": "$cliente_id",
                "media_nota": {"$avg": "$nota"},
                "total_avaliacoes": {"$sum": 1},
                "produtos_distintos": {"$addToSet": "$produto_id"}
            }
        },
        {
            "$project": {
                "cliente_id": "$_id",
                "_id": 0,
                "media_nota": 1,
                "total_avaliacoes": 1,
                "qtd_produtos_distintos": {"$size": "$produtos_distintos"}
            }
        }
    ]

    dados = list(colecao_avaliacoes.aggregate(pipeline))
    df = pd.DataFrame(dados)

    if df.empty:
        print("Nenhum dado encontrado para clustering.")
        return

    X = df[["media_nota", "total_avaliacoes", "qtd_produtos_distintos"]]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)

    print("\nResultado do Clustering de Clientes:")
    print(df[["cliente_id", "media_nota", "total_avaliacoes", "qtd_produtos_distintos", "cluster"]])

    plt.figure(figsize=(8, 5))
    scatter = plt.scatter(X["media_nota"], X["total_avaliacoes"], c=df["cluster"], cmap="viridis")
    plt.xlabel("Média das Notas")
    plt.ylabel("Total de Avaliações")
    plt.title("Clustering de Clientes")
    plt.grid(True)

    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        cliente_id = df.iloc[index]["cliente_id"]
        sel.annotation.set_text(f"Cliente ID: {cliente_id}")

    plt.show()

def importar_avaliacoes_de_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)  # carrega como lista de dicionários
            if conteudo:
                # Converte datas em strings para objetos datetime
                for a in conteudo:
                    if "data" in a:
                        a["data"] = datetime.fromisoformat(a["data"])
                resultado = colecao_avaliacoes.insert_many(conteudo)
                print(f"{len(resultado.inserted_ids)} avaliações importadas com sucesso.")
            else:
                print("Nenhuma avaliação encontrada no arquivo.")
    except Exception as e:
        print(f"Erro ao importar arquivo JSON: {e}")
        
        
        
        
if __name__ == "__main__":
    importar_avaliacoes_de_json("MongoDB/Avaliacoes.json")
    remover_duplicatas()
    listar_avaliacoes_produto("1")  # substitua por um produto que exista no JSON
    agrupar_clientes_por_comportamento()
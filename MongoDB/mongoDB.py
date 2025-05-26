from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import mplcursors

# --- Conexão MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
db = client["sistema_varejo"] # Nome do banco de dados
colecao_avaliacoes = db["avaliacoes"] # Nome da coleção

# --- Funções básicas ---
def adicionar_avaliacao(cliente_id, produto_id, nota, comentario, data=None):
    avaliacao = {
        "cliente_id": cliente_id,
        "produto_id": produto_id,
        "nota": nota,
        "comentario": comentario,
        "data": data or datetime.now()
    }
    resultado = colecao_avaliacoes.insert_one(avaliacao)
    print(f"Avaliação adicionada com ID: {resultado.inserted_id}")

def listar_avaliacoes_produto(produto_id):
    avaliacoes = colecao_avaliacoes.find({"produto_id": produto_id})
    
    produto_id = str(produto_id)
    
    # Converte o cursor em lista
    avaliacoes = list(colecao_avaliacoes.find({"produto_id": produto_id}))
    
    # Verifica se está vazio
    if not avaliacoes:
        print(f"Produto {produto_id} não possui avaliação.")
        return
    
    # Imprime as avaliações
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

# --- Função para popular dados iniciais ---
def popular_avaliacoes_iniciais():
    if colecao_avaliacoes.count_documents({}) > 0:
        print("A coleção já está populada.")
        return
    dados = [
        (1, 1, '2024-01-20 15:00:00', 5, 'Excelente smartphone! Muito rápido e câmera incrível.'),
        (1, 11, '2024-02-10 10:30:00', 4, 'Ótimo produto, mas achei o preço um pouco alto.'),
        (3, 3, '2024-01-25 14:45:00', 5, 'TV com qualidade de imagem fantástica. Super recomendo!'),
        (6, 2, '2024-01-18 09:15:00', 5, 'Café delicioso, aroma incrível. Compro sempre!'),
        (13, 13, '2024-02-08 16:20:00', 4, 'Tênis confortável, mas esperava mais pela marca.'),
        (11, 5, '2024-01-22 11:00:00', 5, 'Camisa de excelente qualidade. Tecido muito bom.'),
        (19, 7, '2024-01-28 13:30:00', 3, 'Bicicleta boa, mas veio com alguns ajustes a fazer.'),
        (22, 12, '2024-02-05 10:45:00', 5, 'Hidratante maravilhoso! Deixa a pele super macia.'),
        (31, 8, '2024-01-26 15:15:00', 5, 'Livro envolvente, não consegui parar de ler!'),
        (37, 14, '2024-02-12 14:00:00', 5, 'Minha filha adorou! Brinquedo de qualidade.'),
        (2, 10, '2024-01-30 11:30:00', 4, 'Notebook rápido, mas esquenta um pouco durante uso intenso.'),
        (4, 1, '2024-01-19 16:45:00', 5, 'Fone com som excelente, bateria dura bastante.'),
        (16, 4, '2024-01-20 09:00:00', 5, 'Panelas antiaderentes de verdade. Muito satisfeita!'),
        (26, 6, '2024-01-23 14:30:00', 4, 'Livro bom, mas esperava mais do autor.'),
        (35, 9, '2024-02-01 10:15:00', 5, 'Quebra-cabeça desafiador e divertido para toda família.')
    ]
    for cliente_id, produto_id, dt_str, nota, comentario in dados:
        data = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        adicionar_avaliacao(str(cliente_id), str(produto_id), nota, comentario, data)

# --- Clustering de clientes ---
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

    # Seleciona apenas as colunas numéricas para o clustering
    X = df[["media_nota", "total_avaliacoes", "qtd_produtos_distintos"]]

    # Aplica KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)

    print("\nResultado do Clustering de Clientes:")
    print(df[["cliente_id", "media_nota", "total_avaliacoes", "qtd_produtos_distintos", "cluster"]])





    # Gráfico de dispersão
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






# --- Execução Principal ---
if __name__ == "__main__":
    popular_avaliacoes_iniciais()
    
    print("\nAvaliações do produto '1':") 
    listar_avaliacoes_produto("1")  # Exemplo de produto
    
    remover_duplicatas()
    agrupar_clientes_por_comportamento(n_clusters=3)
    plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from postegres import get_dados_para_previsao


def prever_vendas():
    dados = get_dados_para_previsao()

    if not dados:
        print("⚠️ Nenhum dado encontrado para previsão.")
        return

    df = pd.DataFrame(dados)
    df["tempo"] = np.arange(len(df))

    X = df[["tempo"]]
    y = df["total_vendas"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    futuro_tempo = np.arange(len(df), len(df) + 5).reshape(-1, 1)
    previsoes = modelo.predict(futuro_tempo)

    print("\n📈 Previsões para os próximos 5 períodos:")
    for i, p in enumerate(previsoes):
        print(f"Período +{i + 1}: R$ {p:.2f}")

    plt.figure(figsize=(10, 5))
    plt.plot(df["tempo"], y, label="Histórico", marker='o')
    plt.plot(futuro_tempo, previsoes, label="Previsão", linestyle="--", marker='x')
    plt.xlabel("Período")
    plt.ylabel("Total de Vendas (R$)")
    plt.title("Previsão de Vendas")
    plt.legend()
    plt.grid(True)
    plt.show()

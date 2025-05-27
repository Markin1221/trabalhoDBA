from postegres import fetch_vendas_por_hora, prever_vendas

if __name__ == "__main__":
    print("▶️ Consultando vendas por hora (OLAP)...")
    vendas = fetch_vendas_por_hora()
    for venda in vendas:
        print(f"Ano: {venda['ano']}, Mês: {venda['mes']}, Dia: {venda['dia']}, Hora: {venda['hora']}, Total: R$ {venda['total_vendas']}")

    print("\n▶️ Rodando previsão de vendas...")
    prever_vendas()

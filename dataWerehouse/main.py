from postegres import fetch_vendas_por_hora, prever_vendas, fetch_olap_vendas_completo
import pandas as pd



def mostrar_olap():
    dados = fetch_olap_vendas_completo()
    for linha in dados:
        print(f"{linha['ano']}-{linha['mes']:02d}-{linha['dia']:02d} | "
              f"{linha['cidade']}/{linha['estado']} | "
              f"{linha['categoria']} - {linha['marca']} | "
              f"Qtd: {linha['total_quantidade']} | Total: R$ {linha['total_valor']}")

def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Consultar vendas por hora")
        print("2 - Prever vendas")
        print("3 - Exibir análise OLAP completa")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            print("\n▶️ Consultando vendas por hora (OLAP simples)...")
            vendas = fetch_vendas_por_hora()
            for venda in vendas:
                print(f"Ano: {venda['ano']}, Mês: {venda['mes']}, Dia: {venda['dia']}, Hora: {venda['hora']}, Total: R$ {venda['total_vendas']}")
        
        elif escolha == "2":
            print("\n▶️ Rodando previsão de vendas...")
            prever_vendas()
        
        elif escolha == "3":
            print("\n▶️ Exibindo análise OLAP completa das vendas:")
            mostrar_olap()

        elif escolha == "0":
            print("Saindo... Até mais!")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()


from .postegres import fetch_vendas_por_hora, prever_vendas, fetch_olap_vendas_completo
from .postegres import consulta_olap, consulta_olap_dinamica
import pandas as pd

dicionarioProfundidade = {
    1: ["ano"],
    2: ["ano", "mes"],
    3: ["ano", "mes", "dia"]
}

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
        print("3 - Exibir análise OLAP basica")
        print("4 - Exibir análise OLAP completa (consulta OLAP)")
        print("5 - Exibir análise OLAP dinâmica")
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
            print("\n▶️ Exibindo análise OLAP basica das vendas:")
            mostrar_olap()
            
        elif escolha == "4":
            print("\n▶️ Exibindo análise OLAP completa das vendas com consulta:")
            consulta_olap()
            
        elif escolha == "5":
            while True:
                print("voce quer fazer o drill down, o roll up ou o slice ou dice?")
                olap = input("Digite 'drill' ou 'roll', 'slice' ou 'dice' ou 0 pra sair: ").strip().lower()

                if olap == 'drill' or olap == 'roll':
                    consulta_olap_dinamica(agrupamentos=["ano"])
                    profundidade = 1

                    rollDrill = input("Você quer fazer o drill down ou roll up? (drill/roll): ").strip().lower()

                    if rollDrill == 'drill':
                        while profundidade < 3:
                            consulta_olap_dinamica(agrupamentos=[dicionarioProfundidade[profundidade]])
                            profundidade += 1

                    elif rollDrill == 'roll':
                        while profundidade > 1:
                            consulta_olap_dinamica(agrupamentos=[dicionarioProfundidade[profundidade]])
                            profundidade -= 1

                    else:
                        print("Opção inválida. Por favor, escolha entre 'drill' ou 'roll'.")

                elif olap == 'slice':
                    print("\n▶️ Realizando Slice na análise OLAP dinâmica...")

                    # Escolher a profundidade (agrupamento)
                    profundidade = int(input("Escolha a profundidade (1 = Ano, 2 = Ano e Mês, 3 = Ano, Mês e Dia): "))
                    agrupamentos = dicionarioProfundidade.get(profundidade, ["ano"])

                    # Perguntar filtro
                    coluna_filtro = input("Digite a coluna que deseja filtrar (ex: categoria, marca, ano): ").strip().lower()
                    valor_filtro = input(f"Digite o valor que deseja filtrar na coluna '{coluna_filtro}': ").strip()

                    consulta_olap_dinamica(
                        agrupamentos=agrupamentos,
                        filtros={coluna_filtro: valor_filtro}
                    )

                elif olap == 'dice':
                    print("\n▶️ Realizando Dice na análise OLAP dinâmica...")

                    # Escolher a profundidade (agrupamento)
                    profundidade = int(input("Escolha a profundidade (1 = Ano, 2 = Ano e Mês, 3 = Ano, Mês e Dia): "))
                    agrupamentos = dicionarioProfundidade.get(profundidade, ["ano"])

                    # Perguntar múltiplos filtros
                    filtros = {}
                    while True:
                        coluna_filtro = input("Digite a coluna que deseja filtrar (ou digite '0' para parar): ").strip().lower()
                        if coluna_filtro == '0':
                            break
                        valor_filtro = input(f"Digite o valor que deseja filtrar na coluna '{coluna_filtro}': ").strip()
                        filtros[coluna_filtro] = valor_filtro

                    consulta_olap_dinamica(
                        agrupamentos=agrupamentos,
                        filtros=filtros
                    )


                elif olap == '0':
                    print("Saindo da análise OLAP dinâmica...")
                    break

                else:
                    print("Opção inválida. Por favor, escolha entre 'drill', 'roll', 'slice' ou 'dice'.")


        elif escolha == "0":
            print("Saindo... Até mais!")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()


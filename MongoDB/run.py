from . import Principal

def escolherProduto():
    encerrar = ""  
    while encerrar != "e":
        id = input("Digite o ID do produto: ")
        produto = Principal.listar_avaliacoes_produto(id)
        print(produto)
        Principal.agrupar_clientes_por_comportamento()
        Principal.pd.DataFrame()
        encerrar = input("Digite 'e' para encerrar ou qualquer outra tecla para continuar: ")

escolherProduto()

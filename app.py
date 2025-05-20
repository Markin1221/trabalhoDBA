import BD
from classes import Produto, Categoria

if __name__ == '__main__':
    BD.inserir_dados_exemplo()
    BD.listar_produtos()
    BD.remover_produto('produto1')
    print("-----------------------------")
    BD.listar_produtos()
    
    resposta = input("Deseja remover ou adicionar (r/a): ")
    if resposta.lower() == 'r':
        chave_produto = input("Digite a chave do produto que deseja remover: ")
        BD.remover_produto(chave_produto)
        BD.listar_produtos()
    elif resposta.lower() == 'a':
        nome_produto = input("Digite o nome do produto: ")
        descricao_produto = input("Digite a descrição do produto: ")
        preco_produto = float(input("Digite o preço do produto: "))
        categoria_produto = input("Digite a categoria do produto: ")
        
        BD.inserir_produto(nome_produto, descricao_produto, preco_produto, categoria_produto)

        BD.listar_produtos()
        
    
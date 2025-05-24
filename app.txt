import BD
from classes import Produto, Categoria

if __name__ == '__main__':
    BD.listar_produtos()
    BD.remover_produto('produto1')
    print("-----------------------------")
    BD.listar_produtos()
    funcao = input("Deseja editar, consultar, listar produtos ou remover/adicionar? (e/c/l/r): ")
    if funcao == 'e':
        atributo_a_mudar = input("Digite o atributo que deseja mudar (nome, descricao, preco, categoria): ")
        nome_produto = input("Digite o nome do produto que deseja consultar: ")
        BD.consultarProduto(nome_produto)
        novo_valor = input("Digite a nova informação: ")
        if atributo_a_mudar == 'preco':
            novo_valor = float(novo_valor)
        elif atributo_a_mudar == 'categoria':
            novo_valor = Categoria(novo_valor)
        elif atributo_a_mudar == 'nome':
            novo_valor = str(novo_valor)
        elif atributo_a_mudar == 'descricao':
            novo_valor = str(novo_valor)
        BD.editarProduto(nome_produto, atributo_a_mudar, novo_valor)
        BD.listar_produtos()
        
        
    elif funcao == 'c':
        print("Você escolheu consultar um produto.")
        nome_produto = input("Digite o nome do produto que deseja consultar: ")
        BD.consultarProduto(nome_produto)
        
        
    elif funcao == 'l':
        print("Você escolheu listar produtos.")
        BD.listar_produtos()
        
        
        
        
    elif funcao == 'r':
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
        
    
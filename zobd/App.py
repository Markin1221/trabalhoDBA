from . import BD

from .classes import Categoria


def menu():
    print("\n--- MENU LOJA ---")
    print("1 - Listar Produtos")
    print("2 - Consultar Produto")
    print("3 - Editar Produto")
    print("4 - Adicionar Produto")
    print("5 - Remover Produto")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def obter_categoria_existente():
    BD.listar_categorias()
    nome_categoria = input("Digite o nome da categoria: ")
    if nome_categoria in BD.listar_categorias(retornar=True):
        return nome_categoria
    else:
        print("Categoria não encontrada.")
        return None

if __name__ == '__main__':
    while True:
        opcao = menu()

        if opcao == '1':
            BD.listar_produtos()

        elif opcao == '2':
            nome = input("Digite o nome do produto para consultar: ")
            BD.consultar_produto(nome)

        elif opcao == '3':
            nome = input("Digite o nome do produto que deseja editar: ")
            BD.consultar_produto(nome)

            print("\nAtributos editáveis: nome_produto, descricao, preco_atual, marca, unidade_medida, ativo, categoria")
            atributo = input("Digite o atributo que deseja alterar: ")

            novo_valor = input("Digite a nova informaçao: ")

            if atributo == "preco_atual":
                novo_valor = float(novo_valor)
            elif atributo == "ativo":
                novo_valor = novo_valor.lower() in ['true', '1', 'sim', 's']
            elif atributo == "categoria":
                if novo_valor not in BD.listar_categorias(retornar=True):
                    print(f"A categoria '{novo_valor}' não existe.")
                    continue

            BD.editar_produto(nome, atributo, novo_valor)

        elif opcao == '4':
            id_produto = input("ID do Produto: ")
            print("--------------------------")
            codigo = input("Código do Produto: ")
            print("--------------------------")
            nome = input("Nome do Produto: ")
            print("--------------------------")
            descricao = input("Descrição do Produto: ")
            print("--------------------------")
            preco = float(input("Preço atual: "))
            print("--------------------------")
            marca = input("Marca: ")
            print("--------------------------")
            unidade = input("Unidade de Medida: ")
            print("Categorias disponíveis:")
            BD.listar_categorias()
            print("--------------------------")
            categoria_nome = input("Categoria do Produto: ")

            categorias_existentes = BD.listar_categorias(retornar=True)
            BD.inserir_produto(id_produto, codigo, nome, descricao, preco, categoria_nome, marca, unidade)
            print(f"Produto '{nome}' cadastrado com sucesso na categoria '{categoria_nome}'.")
            BD.listar_produtos()




            
        elif opcao == '5':
            nome = input("Digite o id do produto que deseja remover: ")
            BD.remover_produto(nome)

        elif opcao == '0':
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida, tente novamente.")

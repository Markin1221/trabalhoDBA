import ZODB
import ZODB.FileStorage
from BTrees.OOBTree import OOBTree
import transaction
from classes import Produto, Categoria


def inicializar_banco(banco_path='loja.fs'):
    storage = ZODB.FileStorage.FileStorage(banco_path)
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()

    if not hasattr(root, 'produtos'):
        root.produtos = OOBTree()
    if not hasattr(root, 'categorias'):
        root.categorias = OOBTree()

    return db, connection, root

def inserir_produto(nome, descricao, preco, categoria_nome, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if categoria_nome not in root.categorias:
            print(f"Categoria '{categoria_nome}' não encontrada.")
            return

        categoria = root.categorias[categoria_nome]
        produto = Produto(nome, descricao, preco, categoria)
        root.produtos[nome] = produto
        transaction.commit()
        print(f"Produto '{nome}' inserido com sucesso.")
    finally:
        connection.close()
        db.close()
        
def inserir_dados_exemplo():
    db, connection, root = inicializar_banco()
    try:
        cat = Categoria("Eletrônicos")
        root.categorias['eletronicos'] = cat
        global p1
        p1 = Produto("Android5G", "celula do android la", 1999.90, cat)
        
        p2 = Produto("aifone", "celular da maçazinha", 5999.90, cat)

        root.produtos['produto1'] = p1
        root.produtos['produto2'] = p2
        
        transaction.commit()
        print("Produtos inseridos com sucesso.")
    finally:
        connection.close()
        db.close()

def remover_produto(nome_produto, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        chave_para_remover = None
        for chave, produto in root.produtos.items():
            if produto.nome.lower() == nome_produto.lower():
                chave_para_remover = chave
                break

        if chave_para_remover:
            del root.produtos[chave_para_remover]
            transaction.commit()
            print(f"Produto com nome '{nome_produto}' removido com sucesso.")
        else:
            print(f"Produto com nome '{nome_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()


def listar_produtos(banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if not hasattr(root, 'produtos') or not root.produtos:
            print("Nenhum produto cadastrado.")
            return

        for chave, produto in root.produtos.items():
            print(f"{chave}: {produto.nome} | {produto.descricao} | R${produto.preco:.2f} | Categoria: {produto.categoria.nome}")
    finally:
        connection.close()
        db.close()

def editarProduto(nome_produto, atributo, novo_valor, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        encontrado = False
        for produto in root.produtos.values():
            if produto.nome.lower() == nome_produto.lower():
                if hasattr(produto, atributo):
                    setattr(produto, atributo, novo_valor)
                    print(f"Atributo '{atributo}' do produto '{nome_produto}' atualizado para: {novo_valor}")
                    connection.transaction_manager.commit()  # Salva as alterações
                    encontrado = True
                    break
                else:
                    print(f"O atributo '{atributo}' não existe nesse produto.")
                    encontrado = True
                    break
        if not encontrado:
            print(f"Produto com nome '{nome_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()

    
     
def consultarProduto(nome_produto, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        encontrado = False
        for produto in root.produtos.values():
            if produto.nome.lower() == nome_produto.lower():
                print(f"Produto encontrado: {produto.nome} | {produto.descricao} | R${produto.preco:.2f} | Categoria: {produto.categoria.nome}")
                encontrado = True
                break
        if not encontrado:
            print(f"Produto com nome '{nome_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()


if __name__ == '__main__':
    inserir_dados_exemplo()
    p1.printar()


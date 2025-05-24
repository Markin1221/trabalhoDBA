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


def inserir_categoria(id_categoria, nome_categoria, descricao=None, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if id_categoria in root.categorias:
            print(f"Categoria com ID '{id_categoria}' já existe.")
            return

        categoria = Categoria(id_categoria, nome_categoria, descricao)
        root.categorias[id_categoria] = categoria
        transaction.commit()
        print(f"Categoria '{nome_categoria}' inserida com sucesso.")
    finally:
        connection.close()
        db.close()


def inserir_produto(id_produto, codigo_produto, nome_produto, descricao, preco_atual,
                    id_categoria, marca, unidade_medida, ativo=True, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if id_categoria not in root.categorias:
            print(f"Categoria com ID '{id_categoria}' não encontrada.")
            return

        categoria = root.categorias[id_categoria]

        if id_produto in root.produtos:
            print(f"Produto com ID '{id_produto}' já existe.")
            return

        produto = Produto(id_produto, codigo_produto, nome_produto, descricao, preco_atual,
                           categoria, marca, unidade_medida, ativo)

        root.produtos[id_produto] = produto
        transaction.commit()
        print(f"Produto '{nome_produto}' inserido com sucesso.")
    finally:
        connection.close()
        db.close()


def remover_produto(id_produto, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if id_produto in root.produtos:
            produto = root.produtos[id_produto]
            # Remove da categoria também
            if produto in produto.categoria.produtos:
                produto.categoria.produtos.remove(produto)

            del root.produtos[id_produto]
            transaction.commit()
            print(f"Produto com ID '{id_produto}' removido com sucesso.")
        else:
            print(f"Produto com ID '{id_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()


def listar_produtos(banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if not root.produtos:
            print("Nenhum produto cadastrado.")
            return

        for id_produto, produto in root.produtos.items():
            print(f"ID: {id_produto}| Nome: {produto.nome_produto} | Descrição: {produto.descricao} | "
                  f"Preço: R${produto.preco_atual:.2f} | Categoria: {produto.categoria.nome_categoria} | "
                  f"Marca: {produto.marca} | Unidade: {produto.unidade_medida} | Ativo: {produto.ativo}")
    finally:
        connection.close()
        db.close()

def listar_categorias(retornar=False, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if not root.categorias:
            print("Nenhuma categoria cadastrada.")
            return [] if retornar else None

        if retornar:
            return list(root.categorias.keys())  # retorna IDs das categorias, ex: ['C1', 'C2']

        print("--- Categorias Cadastradas ---")
        for id_categoria, categoria in root.categorias.items():
            print(f"ID: {id_categoria} | Nome: {categoria.nome_categoria} | Descrição: {categoria.descricao}")
    finally:
        connection.close()
        db.close()

def editar_produto(id_produto, atributo, novo_valor, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if id_produto not in root.produtos:
            print(f"Produto com ID '{id_produto}' não encontrado.")
            return

        produto = root.produtos[id_produto]

        if atributo == 'categoria':
            if novo_valor not in root.categorias:
                print(f"Categoria com ID '{novo_valor}' não encontrada.")
                return
            # Remove da categoria antiga
            if produto in produto.categoria.produtos:
                produto.categoria.produtos.remove(produto)

            nova_categoria = root.categorias[novo_valor]
            produto.categoria = nova_categoria
            nova_categoria.produtos.append(produto)
            print(f"Categoria do produto '{produto.nome_produto}' atualizada.")
        elif hasattr(produto, atributo):
            setattr(produto, atributo, novo_valor)
            print(f"Atributo '{atributo}' do produto '{produto.nome_produto}' atualizado para '{novo_valor}'.")
        else:
            print(f"O atributo '{atributo}' não existe.")
            return

        transaction.commit()

    finally:
        connection.close()
        db.close()


def consultar_produto(id_produto, banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        if id_produto in root.produtos:
            produto = root.produtos[id_produto]
            print(f"ID: {id_produto}| Nome: {produto.nome_produto} | Descrição: {produto.descricao} | "
                  f"Preço: R${produto.preco_atual:.2f} | Categoria: {produto.categoria.nome_categoria} | "
                  f"Marca: {produto.marca} | Unidade: {produto.unidade_medida} | Ativo: {produto.ativo}")
        else:
            print(f"Produto com ID '{id_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()


def inserir_dados_exemplo():
    db, connection, root = inicializar_banco()
    try:
        # Inserindo categorias
        cat = Categoria("C1", "Eletrônicos", "Categoria de eletrônicos")
        root.categorias[cat.id_categoria] = cat

        # Inserindo produtos
        p1 = Produto("P1", "0001", "Smartphone Android", "Celular Android 5G", 1999.90,
                     cat, "Samsung", "Unidade")
        p2 = Produto("P2", "0002", "iPhone", "Celular da maçã", 5999.90,
                     cat, "Apple", "Unidade")

        root.produtos[p1.id_produto] = p1
        root.produtos[p2.id_produto] = p2

        transaction.commit()
        print("Categorias e produtos de exemplo inseridos com sucesso.")
    finally:
        connection.close()
        db.close()


if __name__ == '__main__':
    inserir_dados_exemplo()
    listar_produtos()

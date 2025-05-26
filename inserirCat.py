import ZODB
import ZODB.FileStorage
from BTrees.OOBTree import OOBTree
import transaction
from classes import Produto, Categoria, Fornecedor, ProdutoFornecedor, Estoque, Promocao, ProdutoPromocao
from ZODB import FileStorage, DB


def inicializar_banco(banco_path='loja.fs'):
    storage = FileStorage.FileStorage(banco_path)
    db = DB(storage)
    connection = db.open()
    root = connection.root()

    # Criar coleções OOBTree no root para armazenar cada entidade
    if not hasattr(root, 'categorias'):
        root.categorias = OOBTree()          # key: id_categoria, value: Categoria
    if not hasattr(root, 'produtos'):
        root.produtos = OOBTree()            # key: id_produto, value: Produto
    if not hasattr(root, 'fornecedores'):
        root.fornecedores = OOBTree()       # key: cnpj, value: Fornecedor
    if not hasattr(root, 'produto_fornecedor'):
        root.produto_fornecedor = OOBTree() # key: (id_produto, cnpj), value: ProdutoFornecedor
    if not hasattr(root, 'estoques'):
        root.estoques = OOBTree()            # key: (id_produto, loja), value: Estoque
    if not hasattr(root, 'promocoes'):
        root.promocoes = OOBTree()           # key: nome_promocao, value: Promocao
    if not hasattr(root, 'produto_promocao'):
        root.produto_promocao = OOBTree()    # key: (id_produto, nome_promocao), value: ProdutoPromocao

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
        produtos = getattr(root, 'produtos', None)
        if produtos is None or len(produtos) == 0:
            print("Nenhum produto cadastrado.")
            return

        for id_produto, produto in produtos.items():
            print(f"ID: {id_produto} | Nome: {produto.nome_produto} | Descrição: {produto.descricao} | "
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
            return list(root.categorias.keys())

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
            print(f"ID: {id_produto} | Nome: {produto.nome_produto} | Descrição: {produto.descricao} | "
                  f"Preço: R${produto.preco_atual:.2f} | Categoria: {produto.categoria.nome_categoria} | "
                  f"Marca: {produto.marca} | Unidade: {produto.unidade_medida} | Ativo: {produto.ativo}")
        else:
            print(f"Produto com ID '{id_produto}' não encontrado.")
    finally:
        connection.close()
        db.close()


def inserir_categorias(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    categorias = [
        (1, 'Eletrônicos'),
        (2, 'Informática'),
        (3, 'Alimentos'),
        (4, 'Calçados'),
        (5, 'Utensílios Domésticos'),
        (6, 'Higiene Pessoal'),
        (7, 'Brinquedos'),
        (8, 'Livros'),
        (9, 'Áudio'),
        (10, 'Eletrodomésticos'),
    ]

    if not hasattr(banco, 'categorias'):
        banco.categorias = OOBTree()

    for id_categoria, nome_categoria in categorias:
        if id_categoria not in banco.categorias:
            categoria = Categoria(id_categoria, nome_categoria)
            banco.categorias[id_categoria] = categoria

    banco._p_changed = True
    transaction.commit()

    connection.close()
    db.close()


def inserir_produtos_base(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    produtos = [
        (1, 'Smart TV Samsung 50"', 1),
        (2, 'Notebook Dell Inspiron', 2),
        (3, 'Tablet Samsung Galaxy Tab', 1),
        (4, 'Caixa de Som JBL', 9),
        (5, 'Filtro de Água Melitta', 10),
        (6, 'Cafeteira Melitta', 10),
        (7, 'Leite Nestlé Integral', 3),
        (8, 'Achocolatado Nestlé', 3),
        (13, 'Tênis Nike Air Max', 4),
        (16, 'Jogo de Facas Tramontina', 5),
        (21, 'Sabonete P&G', 6),
        (22, 'Shampoo P&G', 6),
        (25, 'Perfume P&G', 6),
        (31, 'Livro Intrínseca: O Poder do Hábito', 8),
        (37, 'Boneca Mattel', 7),
        (40, 'Carrinho Mattel', 7)
    ]

    if not hasattr(banco, 'produtos'):
        banco.produtos = OOBTree()

    for id_produto, nome_produto, id_categoria in produtos:
        categoria_obj = banco.categorias.get(id_categoria)
        if not categoria_obj:
            print(f"[ERRO] Categoria ID {id_categoria} não encontrada para produto {nome_produto}")
            continue

        produto = Produto(
            id_produto=id_produto,
            codigo_produto=f"C{id_produto:05d}",
            nome_produto=nome_produto,
            descricao=f"Descrição do produto {nome_produto}",
            preco_atual=100.0,
            categoria=categoria_obj,
            marca="Marca Genérica",
            unidade_medida="un",
            ativo=True
        )

        banco.produtos[id_produto] = produto

    banco._p_changed = True
    transaction.commit()

    connection.close()
    db.close()


def inserir_fornecedores(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    fornecedores = [
        ('12345678000100', 'Samsung Eletrônicos do Brasil LTDA', 'Samsung Brasil', '11-5644-2000', 'contato@samsung.com.br', 'Av. Dr. Chucri Zaidan, 1240', 'São Paulo', 'SP'),
        ('23456789000111', 'Dell Computadores do Brasil LTDA', 'Dell Brasil', '11-5503-5000', 'vendas@dell.com.br', 'Av. Industrial, 700', 'Eldorado do Sul', 'RS'),
        ('34567890000122', 'Nestlé Brasil LTDA', 'Nestlé', '11-2199-2999', 'faleconosco@nestle.com.br', 'Av. Nações Unidas, 12495', 'São Paulo', 'SP'),
        ('45678901000133', 'Nike do Brasil Com. e Part. LTDA', 'Nike Brasil', '11-5102-4400', 'atendimento@nike.com.br', 'Av. das Nações Unidas, 14261', 'São Paulo', 'SP'),
        ('56789012000144', 'Tramontina S.A.', 'Tramontina', '54-3461-8200', 'sac@tramontina.com.br', 'Rod. RS-324 Km 2,5', 'Carlos Barbosa', 'RS'),
        ('67890123000155', 'Procter & Gamble do Brasil S.A.', 'P&G Brasil', '11-3046-5800', 'atendimento@pg.com.br', 'Av. Brigadeiro Faria Lima, 3900', 'São Paulo', 'SP'),
        ('78901234000166', 'Mattel do Brasil LTDA', 'Mattel', '11-5090-8500', 'sac@mattel.com.br', 'Av. Tamboré, 1400', 'Barueri', 'SP'),
        ('89012345000177', 'Editora Intrínseca LTDA', 'Intrínseca', '21-2206-7400', 'contato@intrinseca.com', 'Rua Marquês de São Vicente, 99', 'Rio de Janeiro', 'RJ'),
        ('90123456000188', 'JBL do Brasil', 'JBL', '11-3048-1700', 'suporte@jbl.com.br', 'Rua James Clerk Maxwell, 170', 'Campinas', 'SP'),
        ('01234567000199', 'Melitta do Brasil', 'Melitta', '47-3801-5000', 'sac@melitta.com.br', 'Rua Dona Francisca, 8300', 'Joinville', 'SC')
    ]

    if not hasattr(banco, 'fornecedores'):
        banco.fornecedores = OOBTree()

    for cnpj, razao_social, nome_fantasia, telefone, email, endereco, cidade, estado in fornecedores:
        fornecedor = Fornecedor(
            cnpj=cnpj,
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            telefone=telefone,
            email=email,
            endereco=endereco,
            cidade=cidade,
            estado=estado
        )
        banco.fornecedores[cnpj] = fornecedor

    banco._p_changed = True
    transaction.commit()

    connection.close()
    db.close()


def inserir_produtos_fornecedores(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    relacoes = [
        # Samsung
        (1, '12345678000100', 2800.00, 7),
        (3, '12345678000100', 1800.00, 10),

        # Dell
        (2, '23456789000111', 2300.00, 15),

        # Nestlé
        (7, '34567890000122', 20.00, 5),
        (8, '34567890000122', 6.50, 5),

        # Nike
        (13, '45678901000133', 320.00, 10),

        # Tramontina
        (16, '56789012000144', 240.00, 7),

        # P&G
        (21, '67890123000155', 14.50, 5),
        (22, '67890123000155', 19.00, 5),
        (25, '67890123000155', 69.90, 7),

        # Mattel
        (37, '78901234000166', 120.00, 10),
        (40, '78901234000166', 9.90, 5),

        # Intrínseca
        (31, '89012345000177', 39.00, 7),

        # JBL
        (4, '90123456000188', 199.00, 5),

        # Melitta
        (6, '01234567000199', 19.90, 3)
    ]

    if not hasattr(banco, 'produto_fornecedor'):
        banco.produto_fornecedor = OOBTree()

    for id_produto, cnpj_fornecedor, preco_compra, prazo_entrega in relacoes:
        produto_obj = banco.produtos.get(id_produto)
        fornecedor_obj = banco.fornecedores.get(cnpj_fornecedor)

        if not produto_obj:
            print(f"[ERRO] Produto com ID {id_produto} não encontrado.")
            continue

        if not fornecedor_obj:
            print(f"[ERRO] Fornecedor com CNPJ {cnpj_fornecedor} não encontrado.")
            continue

        chave_relacao = (id_produto, cnpj_fornecedor)

        if chave_relacao in banco.produto_fornecedor:
            print(f"[AVISO] Relação Produto {id_produto} e Fornecedor {cnpj_fornecedor} já existe. Pulando.")
            continue

        pf = ProdutoFornecedor(
            produto=produto_obj,
            fornecedor=fornecedor_obj,
            preco_compra=preco_compra,
            prazo_entrega=prazo_entrega
        )

        banco.produto_fornecedor[chave_relacao] = pf
        print(f"[SUCESSO] Relação Produto {id_produto} com Fornecedor {cnpj_fornecedor} inserida.")

    banco._p_changed = True
    transaction.commit()
    print("[INFO] Inserção de produtos-fornecedores concluída com sucesso.")

    connection.close()
    db.close()


def inserir_fornecedores(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    fornecedores = [
        ('12345678000100', 'Samsung Eletrônicos do Brasil LTDA', 'Samsung Brasil', '11-5644-2000', 'contato@samsung.com.br', 'Av. Dr. Chucri Zaidan, 1240', 'São Paulo', 'SP'),
        ('23456789000111', 'Dell Computadores do Brasil LTDA', 'Dell Brasil', '11-5503-5000', 'vendas@dell.com.br', 'Av. Industrial, 700', 'Eldorado do Sul', 'RS'),
        ('34567890000122', 'Nestlé Brasil LTDA', 'Nestlé', '11-2199-2999', 'faleconosco@nestle.com.br', 'Av. Nações Unidas, 12495', 'São Paulo', 'SP'),
        ('45678901000133', 'Nike do Brasil Com. e Part. LTDA', 'Nike Brasil', '11-5102-4400', 'atendimento@nike.com.br', 'Av. das Nações Unidas, 14261', 'São Paulo', 'SP'),
        ('56789012000144', 'Tramontina S.A.', 'Tramontina', '54-3461-8200', 'sac@tramontina.com.br', 'Rod. RS-324 Km 2,5', 'Carlos Barbosa', 'RS'),
        ('67890123000155', 'Procter & Gamble do Brasil S.A.', 'P&G Brasil', '11-3046-5800', 'atendimento@pg.com.br', 'Av. Brigadeiro Faria Lima, 3900', 'São Paulo', 'SP'),
        ('78901234000166', 'Mattel do Brasil LTDA', 'Mattel', '11-5090-8500', 'sac@mattel.com.br', 'Av. Tamboré, 1400', 'Barueri', 'SP'),
        ('89012345000177', 'Editora Intrínseca LTDA', 'Intrínseca', '21-2206-7400', 'contato@intrinseca.com.br', 'Rua Marquês de São Vicente, 99', 'Rio de Janeiro', 'RJ'),
        ('90123456000188', 'JBL do Brasil', 'JBL', '11-3048-1700', 'suporte@jbl.com.br', 'Rua James Clerk Maxwell, 170', 'Campinas', 'SP'),
        ('01234567000199', 'Melitta do Brasil', 'Melitta', '47-3801-5000', 'sac@melitta.com.br', 'Rua Dona Francisca, 8300', 'Joinville', 'SC')
    ]

    if 'fornecedores' not in banco:
        banco['fornecedores'] = {}

    for cnpj, razao_social, nome_fantasia, telefone, email, endereco, cidade, estado in fornecedores:
        fornecedor = Fornecedor(
            cnpj=cnpj,
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            telefone=telefone,
            email=email,
            endereco=endereco,
            cidade=cidade,
            estado=estado
        )
        banco['fornecedores'][cnpj] = fornecedor

    banco._p_changed = True
    transaction.commit()

    connection.close()
    db.close()


def inserir_produtos_fornecedores(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    relacoes = [
        # Samsung
        (1, '12345678000100', 2800.00, 7),
        (3, '12345678000100', 1800.00, 10),

        # Dell
        (2, '23456789000111', 2300.00, 15),

        # Nestlé
        (7, '34567890000122', 20.00, 5),
        (8, '34567890000122', 6.50, 5),

        # Nike
        (13, '45678901000133', 320.00, 10),

        # Tramontina
        (16, '56789012000144', 240.00, 7),

        # P&G
        (21, '67890123000155', 14.50, 5),
        (22, '67890123000155', 19.00, 5),
        (25, '67890123000155', 69.90, 7),

        # Mattel
        (37, '78901234000166', 120.00, 10),
        (40, '78901234000166', 9.90, 5),

        # Intrínseca
        (31, '89012345000177', 39.00, 7),

        # JBL
        (4, '90123456000188', 199.00, 5),

        # Melitta
        (6, '01234567000199', 19.90, 3)
    ]

    if 'produto_fornecedor' not in banco:
        banco['produto_fornecedor'] = {}

    for id_produto, cnpj_fornecedor, preco_compra, prazo_entrega in relacoes:
        produto_obj = banco['produtos'].get(id_produto)
        fornecedor_obj = banco['fornecedores'].get(cnpj_fornecedor)

        if not produto_obj:
            print(f"[ERRO] Produto com ID {id_produto} não encontrado.")
            continue

        if not fornecedor_obj:
            print(f"[ERRO] Fornecedor com CNPJ {cnpj_fornecedor} não encontrado.")
            continue

        chave_relacao = (id_produto, cnpj_fornecedor)

        if chave_relacao in banco['produto_fornecedor']:
            print(f"[AVISO] Relação Produto {id_produto} e Fornecedor {cnpj_fornecedor} já existe. Pulando.")
            continue

        pf = ProdutoFornecedor(
            produto=produto_obj,
            fornecedor=fornecedor_obj,
            preco_compra=preco_compra,
            prazo_entrega=prazo_entrega
        )

        banco['produto_fornecedor'][chave_relacao] = pf
        print(f"[SUCESSO] Relação Produto {id_produto} com Fornecedor {cnpj_fornecedor} inserida.")

    banco._p_changed = True
    transaction.commit()
    print("[INFO] Inserção de produtos-fornecedores concluída com sucesso.")

    connection.close()
    db.close()


def popular_banco_completo(banco_path='loja.fs'):
    print("Inserindo categorias...")
    inserir_categorias(banco_path)
    print("Inserindo produtos...")
    inserir_produtos_base(banco_path)
    print("Inserindo fornecedores...")
    inserir_fornecedores(banco_path)
    print("Inserindo relações produtos-fornecedores...")
    inserir_produtos_fornecedores(banco_path)
    print("Banco populado com sucesso!")


if __name__ == '__main__':
    popular_banco_completo('loja.fs')
    listar_produtos('loja.fs')


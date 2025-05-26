import ZODB
import ZODB.FileStorage
from BTrees.OOBTree import OOBTree
import transaction
from classes import Produto, Categoria,Fornecedor,ProdutoFornecedor,Estoque,Promocao,ProdutoPromocao


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree

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
        if not root.produtos:
            print("Nenhum produto cadastrado.")
            return

        for id_produto, produto in root.produtos.items():
            print(f"ID: {id_produto}| Nome: {produto.nome_produto} | Descrição: {produto.descricao} | "
                  f"Preço: R${produto.preco_atual:.2f} | Categoria: {produto.categoria.nome_categoria} | "
                  f"Marca: {produto.marca} | Unidade: {produto.unidade_medida} | Ativo: {produto.ativo}")
    finally:
        transaction.abort()
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


def inserir_dado_exemplo():
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



def inserir_categorias_iniciais(banco_path='loja.fs'):
    db, connection, root = inicializar_banco()
    categorias_iniciais = [
        ('Eletrônicos', 'Produtos eletrônicos, tecnologia e informática'),
        ('Alimentos e Bebidas', 'Produtos alimentícios, bebidas e snacks'),
        ('Vestuário', 'Roupas, calçados e acessórios'),
        ('Casa e Decoração', 'Móveis, decoração e utilidades domésticas'),
        ('Esportes e Lazer', 'Produtos esportivos e equipamentos de lazer'),
        ('Beleza e Cuidados', 'Cosméticos, perfumaria e cuidados pessoais'),
        ('Livros e Papelaria', 'Livros, material escolar e escritório'),
        ('Brinquedos', 'Brinquedos e jogos infantis'),
    ]

    db, connection, root = inicializar_banco(banco_path)
    try:
        # Se a árvore categorias não existir, criar
        if not hasattr(root, 'categorias'):
            root.categorias = OOBTree()

        # Usar IDs automáticos simples: C1, C2, C3 ...
        proximo_id = 1
        for nome, descricao in categorias_iniciais:
            id_categoria = f"C{proximo_id}"
            if id_categoria in root.categorias:
                print(f"Categoria com ID '{id_categoria}' já existe. Pulando...")
                proximo_id += 1
                continue

            categoria = Categoria(id_categoria, nome, descricao)
            root.categorias[id_categoria] = categoria
            print(f"Categoria '{nome}' inserida com ID '{id_categoria}'.")
            proximo_id += 1

        transaction.commit()
    finally:
        connection.close()
        db.close()



def inserir_categorias_e_produtos(banco_path='loja.fs'):
    db, connection, root = inicializar_banco(banco_path)
    try:
        # Inserir categorias
        categorias = [
            (1, 'Eletrônicos', 'Produtos eletrônicos, tecnologia e informática'),
            (2, 'Alimentos e Bebidas', 'Produtos alimentícios, bebidas e snacks'),
            (3, 'Vestuário', 'Roupas, calçados e acessórios'),
            (4, 'Casa e Decoração', 'Móveis, decoração e utilidades domésticas'),
            (5, 'Esportes e Lazer', 'Produtos esportivos e equipamentos de lazer'),
            (6, 'Beleza e Cuidados', 'Cosméticos, perfumaria e cuidados pessoais'),
            (7, 'Livros e Papelaria', 'Livros, material escolar e escritório'),
            (8, 'Brinquedos', 'Brinquedos e jogos infantis'),
        ]

        for id_cat, nome, desc in categorias:
            if id_cat not in root.categorias:
                root.categorias[id_cat] = Categoria(id_cat, nome, desc)

        # Inserir produtos
        produtos = [
            # Eletrônicos (categoria 1)
            ('P1', 'ELET001', 'Smartphone Galaxy S22', 'Smartphone Samsung Galaxy S22 128GB', 3499.00, 1, 'Samsung', 'UN'),
            ('P2', 'ELET002', 'Notebook Dell Inspiron 15', 'Notebook Dell i5 8GB RAM 512GB SSD', 2899.00, 1, 'Dell', 'UN'),
            ('P3', 'ELET003', 'TV Smart 50" 4K', 'Smart TV LG 50 polegadas 4K', 2199.00, 1, 'LG', 'UN'),
            ('P4', 'ELET004', 'Fone Bluetooth', 'Fone de ouvido bluetooth JBL', 249.90, 1, 'JBL', 'UN'),
            ('P5', 'ELET005', 'Mouse Gamer', 'Mouse gamer RGB Logitech', 199.90, 1, 'Logitech', 'UN'),

            # Alimentos e Bebidas (categoria 2)
            ('P6', 'ALIM001', 'Café Premium 500g', 'Café torrado e moído premium', 24.90, 2, 'Melitta', 'PCT'),
            ('P7', 'ALIM002', 'Chocolate ao Leite 200g', 'Chocolate ao leite Nestlé', 8.90, 2, 'Nestlé', 'UN'),
            ('P8', 'ALIM003', 'Água Mineral 1,5L', 'Água mineral sem gás', 2.90, 2, 'Crystal', 'UN'),
            ('P9', 'ALIM004', 'Biscoito Integral', 'Biscoito integral multigrãos', 4.50, 2, 'Vitarella', 'PCT'),
            ('P10', 'ALIM005', 'Suco Natural 1L', 'Suco de laranja natural', 7.90, 2, 'Del Valle', 'UN'),

            # Vestuário (categoria 3)
            ('P11', 'VEST001', 'Camisa Polo Masculina', 'Camisa polo algodão masculina', 189.90, 3, 'Lacoste', 'UN'),
            ('P12', 'VEST002', 'Calça Jeans Feminina', "Calça jeans feminina skinny", 259.90, 3, "Levi's", 'UN'),
            ('P13', 'VEST003', 'Tênis Running', 'Tênis para corrida unissex', 399.90, 3, 'Nike', 'PAR'),
            ('P14', 'VEST004', 'Vestido Casual', 'Vestido casual feminino', 119.90, 3, 'Renner', 'UN'),
            ('P15', 'VEST005', 'Mochila Escolar', 'Mochila escolar resistente', 149.90, 3, 'Samsonite', 'UN'),

            # Casa e Decoração (categoria 4)
            ('P16', 'CASA001', 'Jogo de Panelas 5 peças', 'Jogo de panelas antiaderente', 299.90, 4, 'Tramontina', 'JG'),
            ('P17', 'CASA002', 'Edredom Casal', 'Edredom casal 100% algodão', 189.90, 4, 'Santista', 'UN'),
            ('P18', 'CASA003', 'Conjunto de Toalhas', 'Kit 4 toalhas de banho', 99.90, 4, 'Karsten', 'KIT'),
            ('P19', 'CASA004', 'Luminária de Mesa', 'Luminária LED para mesa', 89.90, 4, 'Philips', 'UN'),
            ('P20', 'CASA005', 'Organizador Multiuso', 'Organizador plástico com divisórias', 39.90, 4, 'Ordene', 'UN'),

            # Esportes e Lazer (categoria 5)
            ('P21', 'ESPO001', 'Bola de Futebol', 'Bola de futebol oficial', 129.90, 5, 'Adidas', 'UN'),
            ('P22', 'ESPO002', 'Kit Halteres 10kg', 'Par de halteres ajustáveis', 199.90, 5, 'Kikos', 'KIT'),
            ('P23', 'ESPO003', 'Tapete Yoga', 'Tapete para yoga antiderrapante', 79.90, 5, 'Acte Sports', 'UN'),
            ('P24', 'ESPO004', 'Bicicleta Aro 29', 'Mountain bike aro 29', 1499.00, 5, 'Caloi', 'UN'),
            ('P25', 'ESPO005', 'Corda de Pular', 'Corda de pular profissional', 39.90, 5, 'Speedo', 'UN'),

            # Beleza e Cuidados (categoria 6)
            ('P26', 'BELZ001', 'Shampoo 400ml', 'Shampoo hidratante', 18.90, 6, 'Pantene', 'UN'),
            ('P27', 'BELZ002', 'Creme Hidratante 200ml', 'Creme hidratante corporal', 24.90, 6, 'Nivea', 'UN'),
            ('P28', 'BELZ003', 'Perfume Masculino 100ml', 'Perfume masculino amadeirado', 189.90, 6, 'Boticário', 'UN'),
            ('P29', 'BELZ004', 'Base Líquida', 'Base líquida cobertura média', 249.90, 6, 'MAC', 'UN'),
            ('P30', 'BELZ005', 'Kit Maquiagem', 'Kit maquiagem completo', 89.90, 6, 'Ruby Rose', 'KIT'),

            # Livros e Papelaria (categoria 7)
            ('P31', 'LIVR001', 'Livro Best Seller', 'Romance contemporâneo', 49.90, 7, 'Intrínseca', 'UN'),
            ('P32', 'LIVR002', 'Caderno Universitário', 'Caderno 200 folhas', 24.90, 7, 'Tilibra', 'UN'),
            ('P33', 'LIVR003', 'Kit Canetas Coloridas', 'Kit 12 canetas coloridas', 19.90, 7, 'BIC', 'KIT'),
            ('P34', 'LIVR004', 'Agenda 2024', 'Agenda executiva 2024', 34.90, 7, 'Foroni', 'UN'),
            ('P35', 'LIVR005', 'Calculadora Científica', 'Calculadora científica completa', 89.90, 7, 'Casio', 'UN'),

            # Brinquedos (categoria 8)
            ('P36', 'BRIN001', 'Lego Classic 500 peças', 'Kit Lego construção classic', 299.90, 8, 'Lego', 'CX'),
            ('P37', 'BRIN002', 'Boneca Fashion', 'Boneca fashion com acessórios', 149.90, 8, 'Mattel', 'UN'),
            ('P38', 'BRIN003', 'Quebra-cabeça 1000 peças', 'Quebra-cabeça paisagem', 59.90, 8, 'Grow', 'CX'),
            ('P39', 'BRIN004', 'Carrinho Hot Wheels', 'Carrinho colecionável', 12.90, 8, 'Hot Wheels', 'UN'),
            ('P40', 'BRIN005', 'Jogo de Tabuleiro', 'Jogo War clássico', 89.90, 8, 'Grow', 'CX'),
        ]

        for id_produto, codigo, nome, descricao, preco, id_cat, marca, unidade in produtos:
            if id_produto not in root.produtos:
                categoria = root.categorias.get(id_cat)
                if categoria is None:
                    print(f"Categoria {id_cat} não encontrada para o produto {nome}. Ignorando.")
                    continue
                produto = Produto(id_produto, codigo, nome, descricao, preco,
                                 categoria, marca, unidade, ativo=True)
                root.produtos[id_produto] = produto

        transaction.commit()
        print("Categorias e produtos inseridos com sucesso.")

    finally:
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

# só então feche conexão e banco:
    connection.close()
    db.close()


def inserir_produtos_fornecedores(banco_path='loja.fs'):
    import transaction
    db, connection, banco = inicializar_banco(banco_path)
    relacoes = [
        # Samsung
        (1, 1, 2800.00, 7),
        (3, 1, 1800.00, 10),

        # Dell
        (2, 2, 2300.00, 15),

        # Nestlé
        (7, 3, 20.00, 5),
        (8, 3, 6.50, 5),

        # Nike
        (13, 4, 320.00, 10),

        # Tramontina
        (16, 5, 240.00, 7),

        # P&G
        (21, 6, 14.50, 5),
        (22, 6, 19.00, 5),
        (25, 6, 69.90, 7),

        # Mattel
        (37, 7, 120.00, 10),
        (40, 7, 9.90, 5),

        # Intrínseca
        (31, 8, 39.00, 7),

        # JBL
        (4, 9, 199.00, 5),

        # Melitta
        (6, 10, 19.90, 3)
    ]

    if 'produto_fornecedor' not in banco:
        banco['produto_fornecedor'] = {}

    for id_produto, id_fornecedor, preco_compra, prazo_entrega in relacoes:
        produto_obj = banco.produtos.get(id_produto)
        fornecedor_obj = banco['fornecedores'].get(id_fornecedor)

        if not produto_obj or not fornecedor_obj:
            print(f"Produto ou fornecedor não encontrado: produto {id_produto}, fornecedor {id_fornecedor}")
            continue

        pf = ProdutoFornecedor(
            produto=produto_obj,
            fornecedor=fornecedor_obj,
            preco_compra=preco_compra,
            prazo_entrega=prazo_entrega
        )
        banco['produto_fornecedor'][(id_produto, id_fornecedor)] = pf

    banco._p_changed = True
    transaction.commit()
    connection.close()
    db.close()

def inserir_estoques(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)

    # Verifica se a coleção de produtos existe
    if 'produtos' not in banco:
        print('Nenhum produto cadastrado. Operação de estoque cancelada.')
        connection.close()
        db.close()
        return

    if 'estoque' not in banco:
        banco['estoque'] = OOBTree()

    estoques = [
        (1, 'SP', 25, 5, 50),
        (2, 'SP', 15, 3, 30),
        # ... (resto dos dados)
    ]

    for id_produto, loja, qt_atual, qt_min, qt_max in estoques:
        produto_obj = banco['produtos'].get(id_produto)

        if produto_obj is None:
            print(f"Produto ID {id_produto} não encontrado. Estoque não criado.")
            continue

        estoque_obj = Estoque(
            produto=produto_obj,
            loja=loja,
            quantidade_atual=qt_atual,
            quantidade_minima=qt_min,
            quantidade_maxima=qt_max
        )

        banco['estoque'][(id_produto, loja)] = estoque_obj

    banco._p_changed = True
    transaction.commit()
    connection.close()
    db.close()



def inserir_promocoes(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)
    promocoes = [
        ("Black Friday Eletrônicos", "Desconto especial em eletrônicos selecionados", "2024-11-22", "2024-11-29", 20.00),
        ("Liquida Verão", "Promoção de roupas e acessórios de verão", "2024-01-15", "2024-02-15", 30.00),
        ("Volta às Aulas", "Desconto em material escolar e papelaria", "2024-01-20", "2024-02-28", 15.00),
        ("Semana do Consumidor", "Descontos em todas as categorias", "2024-03-11", "2024-03-17", 10.00),
        ("Dia das Mães", "Promoção especial para presentes", "2024-05-06", "2024-05-12", 25.00),
    ]

    if 'promocao' not in banco:
        banco['promocao'] = {}

    for i, (nome, desc, dt_inicio, dt_fim, perc_desc) in enumerate(promocoes, start=1):
        p = Promocao(
            id=i,
            nome_promocao=nome,
            descricao=desc,
            data_inicio=dt_inicio,
            data_fim=dt_fim,
            percentual_desconto=perc_desc
        )
        banco['promocao'][i] = p

    banco._p_changed = True
    transaction.commit()
    connection.close()
    db.close()


def inserir_produtos_promocao(banco_path='loja.fs'):
    db, connection, banco = inicializar_banco(banco_path)
    produtos_promocao = [
        # Black Friday
        (1, 1, 2799.20),
        (1, 2, 2319.20),
        (1, 3, 1759.20),
        (1, 4, 199.92),
        (1, 5, 159.92),

        # Liquida Verão
        (2, 11, 132.93),
        (2, 12, 181.93),
        (2, 13, 279.93),
        (2, 14, 83.93),
        (2, 15, 104.93),

        # Volta às Aulas
        (3, 31, 42.42),
        (3, 32, 21.17),
        (3, 33, 16.92),
        (3, 34, 29.67),
        (3, 35, 76.42),

        # Semana do Consumidor
        (4, 6, 22.41),
        (4, 7, 16.58),
        (4, 8, 15.08),

        # Dia das Mães
        (5, 9, 51.15),
        (5, 10, 26.18),
    ]

    if 'produto_promocao' not in banco:
        banco['produto_promocao'] = {}

    for id_promocao, id_produto, preco_promocao in produtos_promocao:
        pp = ProdutoPromocao(
            id_promocao=id_promocao,
            id_produto=id_produto,
            preco_promocao=preco_promocao
        )
        banco['produto_promocao'][(id_promocao, id_produto)] = pp

    banco._p_changed = True
    transaction.commit()
    connection.close()
    db.close()

def popular_banco_completo(banco_path='loja.fs'):
    inserir_fornecedores(banco_path)
    inserir_produtos_fornecedores(banco_path)
    inserir_estoques(banco_path)
    inserir_promocoes(banco_path)
    inserir_produtos_promocao(banco_path)




if __name__ == '__main__':
    listar_produtos()
    popular_banco_completo('loja.fs')
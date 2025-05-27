import psycopg2
from psycopg2.extras import RealDictCursor
from config import POSTGRES

def conectar():
    try:
        conn = psycopg2.connect(**POSTGRES)
        cursor = conn.cursor()

        # Função inserir_categorias
        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_categorias()
        RETURNS void AS $$
        BEGIN
            INSERT INTO categoria (nome_categoria, descricao) VALUES
            ('Eletrônicos', 'Produtos eletrônicos, tecnologia e informática'),
            ('Alimentos e Bebidas', 'Produtos alimentícios, bebidas e snacks'),
            ('Vestuário', 'Roupas, calçados e acessórios'),
            ('Casa e Decoração', 'Móveis, decoração e utilidades domésticas'),
            ('Esportes e Lazer', 'Produtos esportivos e equipamentos de lazer'),
            ('Beleza e Cuidados', 'Cosméticos, perfumaria e cuidados pessoais'),
            ('Livros e Papelaria', 'Livros, material escolar e escritório'),
            ('Brinquedos', 'Brinquedos e jogos infantis');
        END;
        $$ LANGUAGE plpgsql;
        """)

        # Função inserir_produtos (separada por categorias para evitar string muito longa)
        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_produtos()
        RETURNS void AS $$
        BEGIN
            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('ELET001', 'Smartphone Galaxy S22', 'Smartphone Samsung Galaxy S22 128GB', 1, 'Samsung', 3499.00, 'UN'),
            ('ELET002', 'Notebook Dell Inspiron 15', 'Notebook Dell i5 8GB RAM 512GB SSD', 1, 'Dell', 2899.00, 'UN'),
            ('ELET003', 'TV Smart 50'' 4K', 'Smart TV LG 50 polegadas 4K', 1, 'LG', 2199.00, 'UN'),
            ('ELET004', 'Fone Bluetooth', 'Fone de ouvido bluetooth JBL', 1, 'JBL', 249.90, 'UN'),
            ('ELET005', 'Mouse Gamer', 'Mouse gamer RGB Logitech', 1, 'Logitech', 199.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('ALIM001', 'Café Premium 500g', 'Café torrado e moído premium', 2, 'Melitta', 24.90, 'PCT'),
            ('ALIM002', 'Chocolate ao Leite 200g', 'Chocolate ao leite Nestlé', 2, 'Nestlé', 8.90, 'UN'),
            ('ALIM003', 'Água Mineral 1,5L', 'Água mineral sem gás', 2, 'Crystal', 2.90, 'UN'),
            ('ALIM004', 'Biscoito Integral', 'Biscoito integral multigrãos', 2, 'Vitarella', 4.50, 'PCT'),
            ('ALIM005', 'Suco Natural 1L', 'Suco de laranja natural', 2, 'Del Valle', 7.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('VEST001', 'Camisa Polo Masculina', 'Camisa polo algodão masculina', 3, 'Lacoste', 189.90, 'UN'),
            ('VEST002', 'Calça Jeans Feminina', 'Calça jeans feminina skinny', 3, 'Levi''s', 259.90, 'UN'),
            ('VEST003', 'Tênis Running', 'Tênis para corrida unissex', 3, 'Nike', 399.90, 'PAR'),
            ('VEST004', 'Vestido Casual', 'Vestido casual feminino', 3, 'Renner', 119.90, 'UN'),
            ('VEST005', 'Mochila Escolar', 'Mochila escolar resistente', 3, 'Samsonite', 149.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('CASA001', 'Jogo de Panelas 5 peças', 'Jogo de panelas antiaderente', 4, 'Tramontina', 299.90, 'JG'),
            ('CASA002', 'Edredom Casal', 'Edredom casal 100% algodão', 4, 'Santista', 189.90, 'UN'),
            ('CASA003', 'Conjunto de Toalhas', 'Kit 4 toalhas de banho', 4, 'Karsten', 99.90, 'KIT'),
            ('CASA004', 'Luminária de Mesa', 'Luminária LED para mesa', 4, 'Philips', 89.90, 'UN'),
            ('CASA005', 'Organizador Multiuso', 'Organizador plástico com divisórias', 4, 'Ordene', 39.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('ESPO001', 'Bola de Futebol', 'Bola de futebol oficial', 5, 'Adidas', 129.90, 'UN'),
            ('ESPO002', 'Kit Halteres 10kg', 'Par de halteres ajustáveis', 5, 'Kikos', 199.90, 'KIT'),
            ('ESPO003', 'Tapete Yoga', 'Tapete para yoga antiderrapante', 5, 'Acte Sports', 79.90, 'UN'),
            ('ESPO004', 'Bicicleta Aro 29', 'Mountain bike aro 29', 5, 'Caloi', 1499.00, 'UN'),
            ('ESPO005', 'Corda de Pular', 'Corda de pular profissional', 5, 'Speedo', 39.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('BELZ001', 'Shampoo 400ml', 'Shampoo hidratante', 6, 'Pantene', 18.90, 'UN'),
            ('BELZ002', 'Creme Hidratante 200ml', 'Creme hidratante corporal', 6, 'Nivea', 24.90, 'UN'),
            ('BELZ003', 'Perfume Masculino 100ml', 'Perfume masculino amadeirado', 6, 'Boticário', 189.90, 'UN'),
            ('BELZ004', 'Base Líquida', 'Base líquida cobertura média', 6, 'MAC', 249.90, 'UN'),
            ('BELZ005', 'Kit Maquiagem', 'Kit maquiagem completo', 6, 'Ruby Rose', 89.90, 'KIT');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('LIVR001', 'Livro Best Seller', 'Romance contemporâneo', 7, 'Intrínseca', 49.90, 'UN'),
            ('LIVR002', 'Caderno Universitário', 'Caderno 200 folhas', 7, 'Tilibra', 24.90, 'UN'),
            ('LIVR003', 'Kit Canetas Coloridas', 'Kit 12 canetas coloridas', 7, 'BIC', 19.90, 'KIT'),
            ('LIVR004', 'Agenda 2024', 'Agenda executiva 2024', 7, 'Foroni', 34.90, 'UN'),
            ('LIVR005', 'Calculadora Científica', 'Calculadora científica completa', 7, 'Casio', 89.90, 'UN');

            INSERT INTO produto (codigo_produto, nome_produto, descricao, id_categoria, marca, preco_atual, unidade_medida) VALUES
            ('BRIN001', 'Lego Classic 500 peças', 'Kit Lego construção classic', 8, 'Lego', 299.90, 'CX'),
            ('BRIN002', 'Boneca Fashion', 'Boneca fashion com acessórios', 8, 'Mattel', 149.90, 'UN'),
            ('BRIN003', 'Quebra-cabeça 1000 peças', 'Quebra-cabeça paisagem', 8, 'Grow', 59.90, 'CX'),
            ('BRIN004', 'Carrinho Hot Wheels', 'Carrinho colecionável', 8, 'Hot Wheels', 12.90, 'UN'),
            ('BRIN005', 'Jogo de Tabuleiro', 'Jogo War clássico', 8, 'Grow', 89.90, 'CX');
        END;
        $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_lojas()
        RETURNS void AS $$
        BEGIN
            INSERT INTO loja (codigo_loja, nome_loja, endereco, cidade, estado, cep, telefone, gerente) VALUES
            ('LJ001', 'Loja Shopping Center', 'Av. Paulista, 1500', 'São Paulo', 'SP', '01310100', '11-3456-7890', 'Carlos Silva'),
            ('LJ002', 'Loja Barra Shopping', 'Av. das Américas, 4666', 'Rio de Janeiro', 'RJ', '22640102', '21-2431-8900', 'Ana Santos'),
            ('LJ003', 'Loja BH Shopping', 'Rod. BR-356, 3049', 'Belo Horizonte', 'MG', '31150900', '31-3456-7890', 'Pedro Oliveira'),
            ('LJ004', 'Loja Recife Shopping', 'Av. Agamenon Magalhães, 1000', 'Recife', 'PE', '52070000', '81-3456-7890', 'Maria Costa'),
            ('LJ005', 'Loja Salvador Shopping', 'Av. Tancredo Neves, 2915', 'Salvador', 'BA', '41820021', '71-3456-7890', 'João Pereira'),
            ('LJ006', 'Loja Porto Alegre', 'Av. Diário de Notícias, 300', 'Porto Alegre', 'RS', '90810000', '51-3456-7890', 'Paula Lima'),
            ('LJ007', 'Loja Brasília Shopping', 'SCN Q 6 L 2', 'Brasília', 'DF', '70716900', '61-3456-7890', 'Roberto Alves'),
            ('LJ008', 'Loja Curitiba Shopping', 'Av. das Torres, 1700', 'Curitiba', 'PR', '82840730', '41-3456-7890', 'Juliana Martins');
        END;
        $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_funcionarios()
        RETURNS void AS $$
        BEGIN
            INSERT INTO funcionario (codigo_funcionario, nome, cargo, id_loja, salario) VALUES
            ('FUNC001', 'Carlos Silva', 'Gerente', 1, 8000.00),
            ('FUNC002', 'Mariana Rocha', 'Vendedor', 1, 2500.00),
            ('FUNC003', 'José Santos', 'Vendedor', 1, 2500.00),
            ('FUNC004', 'Laura Ferreira', 'Caixa', 1, 2200.00),
            ('FUNC005', 'Ana Santos', 'Gerente', 2, 8000.00),
            ('FUNC006', 'Bruno Costa', 'Vendedor', 2, 2500.00),
            ('FUNC007', 'Carla Almeida', 'Vendedor', 2, 2500.00),
            ('FUNC008', 'Diego Pereira', 'Caixa', 2, 2200.00),
            ('FUNC009', 'Pedro Oliveira', 'Gerente', 3, 8000.00),
            ('FUNC010', 'Fernanda Lima', 'Vendedor', 3, 2500.00),
            ('FUNC011', 'Ricardo Silva', 'Vendedor', 3, 2500.00),
            ('FUNC012', 'Tatiana Souza', 'Caixa', 3, 2200.00),
            ('FUNC013', 'Maria Costa', 'Gerente', 4, 8000.00),
            ('FUNC014', 'Anderson Melo', 'Vendedor', 4, 2500.00),
            ('FUNC015', 'Beatriz Nunes', 'Vendedor', 4, 2500.00),
            ('FUNC016', 'Cláudio Ribeiro', 'Caixa', 4, 2200.00),
            ('FUNC017', 'João Pereira', 'Gerente', 5, 8000.00),
            ('FUNC018', 'Sandra Matos', 'Vendedor', 5, 2500.00),
            ('FUNC019', 'Marcos Dias', 'Vendedor', 5, 2500.00),
            ('FUNC020', 'Elaine Barros', 'Caixa', 5, 2200.00);
        END;
        $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_clientes()
        RETURNS void AS $$
        BEGIN
            INSERT INTO cliente (cpf, nome, email, telefone, endereco, cidade, estado, cep) VALUES
            ('12345678901', 'Paulo Henrique Silva', 'paulo.silva@email.com', '11-98765-4321', 'Rua das Flores, 123', 'São Paulo', 'SP', '01234567'),
            ('23456789012', 'Ana Maria Santos', 'ana.santos@email.com', '11-97654-3210', 'Av. Paulista, 456', 'São Paulo', 'SP', '01310100'),
            ('34567890123', 'Roberto Carlos Oliveira', 'roberto.oliveira@email.com', '21-96543-2109', 'Rua Copacabana, 789', 'Rio de Janeiro', 'RJ', '22020050'),
            ('45678901234', 'Juliana Costa Lima', 'juliana.lima@email.com', '31-95432-1098', 'Av. Afonso Pena, 321', 'Belo Horizonte', 'MG', '30130005'),
            ('56789012345', 'Fernando Alves Costa', 'fernando.costa@email.com', '81-94321-0987', 'Av. Boa Viagem, 654', 'Recife', 'PE', '51020180'),
            ('67890123456', 'Mariana Ferreira Souza', 'mariana.souza@email.com', '71-93210-9876', 'Av. Oceânica, 987', 'Salvador', 'BA', '40160060'),
            ('78901234567', 'Alexandre Martins Silva', 'alexandre.silva@email.com', '51-92109-8765', 'Rua da Praia, 147', 'Porto Alegre', 'RS', '90020060'),
            ('89012345678', 'Camila Rodrigues Santos', 'camila.santos@email.com', '61-91098-7654', 'SQS 308 Bloco C', 'Brasília', 'DF', '70355030'),
            ('90123456789', 'Ricardo Pereira Lima', 'ricardo.lima@email.com', '41-90987-6543', 'Rua XV de Novembro, 258', 'Curitiba', 'PR', '80020310'),
            ('01234567890', 'Patricia Almeida Costa', 'patricia.costa@email.com', '11-89876-5432', 'Alameda Santos, 369', 'São Paulo', 'SP', '01419002'),
            ('11223344556', 'Bruno Carvalho Dias', 'bruno.dias@email.com', '21-88765-4321', 'Av. Rio Branco, 741', 'Rio de Janeiro', 'RJ', '20040008'),
            ('22334455667', 'Letícia Nunes Oliveira', 'leticia.oliveira@email.com', '31-87654-3210', 'Rua da Bahia, 852', 'Belo Horizonte', 'MG', '30160011'),
            ('33445566778', 'Carlos Eduardo Santos', 'carlos.santos@email.com', '81-86543-2109', 'Rua do Sol, 963', 'Recife', 'PE', '50030230'),
            ('44556677889', 'Daniela Sousa Lima', 'daniela.lima@email.com', '71-85432-1098', 'Av. Sete de Setembro, 159', 'Salvador', 'BA', '40060500'),
            ('55667788990', 'Marcelo Ferreira Costa', 'marcelo.costa@email.com', '51-84321-0987', 'Av. Ipiranga, 753', 'Porto Alegre', 'RS', '90160091');
        END;
        $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
        CREATE OR REPLACE FUNCTION inserir_fornecedores()
        RETURNS void AS $$
        BEGIN
            INSERT INTO fornecedor (cnpj, razao_social, nome_fantasia, telefone, email, endereco, cidade, estado) VALUES
            ('12345678000100', 'Samsung Eletrônicos do Brasil LTDA', 'Samsung Brasil', '11-5644-2000', 'contato@samsung.com.br', 'Av. Dr. Chucri Zaidan, 1240', 'São Paulo', 'SP'),
            ('23456789000111', 'Dell Computadores do Brasil LTDA', 'Dell Brasil', '11-5503-5000', 'vendas@dell.com.br', 'Av. Industrial, 700', 'Eldorado do Sul', 'RS'),
            ('34567890000122', 'Nestlé Brasil LTDA', 'Nestlé', '11-2199-2999', 'faleconosco@nestle.com.br', 'Av. Nações Unidas, 12495', 'São Paulo', 'SP'),
            ('45678901000133', 'Nike do Brasil Com. e Part. LTDA', 'Nike Brasil', '11-5102-4400', 'atendimento@nike.com.br', 'Av. das Nações Unidas, 14261', 'São Paulo', 'SP'),
            ('56789012000144', 'Tramontina S.A.', 'Tramontina', '54-3461-8200', 'sac@tramontina.com.br', 'Rod. RS-324 Km 2,5', 'Carlos Barbosa', 'RS'),
            ('67890123000155', 'Procter & Gamble do Brasil S.A.', 'P&G Brasil', '11-3046-5800', 'atendimento@pg.com.br', 'Av. Brigadeiro Faria Lima, 3900', 'São Paulo', 'SP'),
            ('78901234000166', 'Mattel do Brasil LTDA', 'Mattel', '11-5090-8500', 'sac@mattel.com.br', 'Av. Tamboré, 1400', 'Barueri', 'SP'),
            ('89012345000177', 'Editora Intrínseca LTDA', 'Intrínseca', '21-2206-7400', 'contato@intrinseca.com.br', 'Rua Marquês de São Vicente, 99', 'Rio de Janeiro', 'RJ'),
            ('90123456000188', 'JBL do Brasil', 'JBL', '11-3048-1700', 'suporte@jbl.com.br', 'Rua James Clerk Maxwell, 170', 'Campinas', 'SP'),
            ('01234567000199', 'Melitta do Brasil', 'Melitta', '47-3801-5000', 'sac@melitta.com.br', 'Rua Dona Francisca, 8300', 'Joinville', 'SC');
        END;
        $$ LANGUAGE plpgsql;
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Funções criadas com sucesso!")

    except Exception as e:
        print("Erro ao conectar ou executar:", e)
        
if __name__ == "__main__":
    conectar()
    try:
        conn = psycopg2.connect(**POSTGRES)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT inserir_categorias();")
        cursor.execute("SELECT inserir_produtos();")
        cursor.execute("SELECT inserir_lojas();")
        cursor.execute("SELECT inserir_funcionarios();")
        cursor.execute("SELECT inserir_clientes();")
        cursor.execute("SELECT inserir_fornecedores();")
        conn.commit()
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print("Erro ao inserir dados:", e)
    finally:
        cursor.close()
        conn.close()
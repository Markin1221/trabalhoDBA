import psycopg2
from psycopg2.extras import RealDictCursor
from config import POSTGRES

# Conectar ao banco
def conectar():
    conn = psycopg2.connect(**POSTGRES)
    print("🔌 Conectado ao banco:", conn.get_dsn_parameters()["dbname"])
    return conn

# Criar tabelas
# Criar tabelas
def criar_categoria(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria SERIAL PRIMARY KEY,
        nome_categoria VARCHAR(50) NOT NULL,
        descricao TEXT
    );
    """)

def criar_produto_fornecedor(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produto_fornecedor (
        id_produto INT,
        id_fornecedor INT,
        preco_compra DECIMAL(10,2),
        prazo_entrega INT,
        PRIMARY KEY (id_produto, id_fornecedor),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor)
    );
    """)


def criar_fornecedor(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fornecedor (
        id_fornecedor SERIAL PRIMARY KEY,
        cnpj VARCHAR(14) UNIQUE NOT NULL,
        razao_social VARCHAR(100) NOT NULL,
        nome_fantasia VARCHAR(100),
        telefone VARCHAR(20),
        email VARCHAR(100),
        endereco VARCHAR(200),
        cidade VARCHAR(50),
        estado CHAR(2),
        ativo BOOLEAN DEFAULT TRUE
    );
    """)


def criar_produto(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id_produto SERIAL PRIMARY KEY,
        codigo_produto VARCHAR(20) UNIQUE NOT NULL,
        nome_produto VARCHAR(100) NOT NULL,
        descricao TEXT,
        id_categoria INT,
        marca VARCHAR(50),
        preco_atual DECIMAL(10,2),
        unidade_medida VARCHAR(20),
        ativo BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
    );
    """)


def criar_loja(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS loja (
        id_loja SERIAL PRIMARY KEY,
        codigo_loja VARCHAR(10) UNIQUE NOT NULL,
        nome_loja VARCHAR(50) NOT NULL,
        endereco VARCHAR(200),
        cidade VARCHAR(50),
        estado CHAR(2),
        cep VARCHAR(8),
        telefone VARCHAR(20),
        gerente VARCHAR(100),
        ativa BOOLEAN DEFAULT TRUE
    );
    """)


def criar_cliente(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente SERIAL PRIMARY KEY,
        cpf VARCHAR(11) UNIQUE NOT NULL,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        telefone VARCHAR(20),
        endereco VARCHAR(200),
        cidade VARCHAR(50),
        estado CHAR(2),
        cep VARCHAR(8),
        ativo BOOLEAN DEFAULT TRUE
    );
    """)


def criar_funcionario(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS funcionario (
        id_funcionario SERIAL PRIMARY KEY,
        codigo_funcionario VARCHAR(10) UNIQUE NOT NULL,
        nome VARCHAR(100) NOT NULL,
        cargo VARCHAR(50),
        id_loja INT,
        salario DECIMAL(10,2),
        ativo BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (id_loja) REFERENCES loja(id_loja)
    );
    """)


def criar_venda(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS venda (
        id_venda SERIAL PRIMARY KEY,
        numero_venda VARCHAR(20) UNIQUE NOT NULL,
        id_cliente INT,
        id_loja INT,
        id_funcionario INT,
        data_venda TIMESTAMP,
        valor_total DECIMAL(10,2),
        desconto_total DECIMAL(10,2),
        forma_pagamento VARCHAR(30),
        status_venda VARCHAR(20),
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
        FOREIGN KEY (id_loja) REFERENCES loja(id_loja),
        FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
    );
    """)


def criar_item_venda(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS item_venda (
        id_item SERIAL PRIMARY KEY,
        id_venda INT,
        id_produto INT,
        quantidade INT,
        preco_unitario DECIMAL(10,2),
        desconto DECIMAL(10,2),
        valor_total DECIMAL(10,2),
        FOREIGN KEY (id_venda) REFERENCES venda(id_venda),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );
    """)
    


def criar_compra(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS compra (
        id_compra SERIAL PRIMARY KEY,
        numero_compra VARCHAR(20) UNIQUE NOT NULL,
        id_fornecedor INT,
        id_loja INT,
        data_compra TIMESTAMP,
        valor_total DECIMAL(10,2),
        status_compra VARCHAR(20),
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor),
        FOREIGN KEY (id_loja) REFERENCES loja(id_loja)
    );
    """)


def criar_item_compra(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS item_compra (
        id_item SERIAL PRIMARY KEY,
        id_compra INT,
        id_produto INT,
        quantidade INT,
        preco_unitario DECIMAL(10,2),
        valor_total DECIMAL(10,2),
        FOREIGN KEY (id_compra) REFERENCES compra(id_compra),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );
    """)


def criar_avaliacao(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS avaliacao (
        id_avaliacao SERIAL PRIMARY KEY,
        id_produto INT,
        id_cliente INT,
        data_avaliacao TIMESTAMP,
        nota INT CHECK (nota >= 1 AND nota <= 5),
        comentario TEXT,
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
    );
    """)


def criar_promocao(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS promocao (
        id_promocao SERIAL PRIMARY KEY,
        nome_promocao VARCHAR(100) NOT NULL,
        descricao TEXT,
        data_inicio DATE,
        data_fim DATE,
        percentual_desconto DECIMAL(5,2),
        ativa BOOLEAN DEFAULT TRUE
    );
    """)


def criar_produto_promocao(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produto_promocao (
        id_promocao INT,
        id_produto INT,
        preco_promocional DECIMAL(10,2),
        PRIMARY KEY (id_promocao, id_produto),
        FOREIGN KEY (id_promocao) REFERENCES promocao(id_promocao),
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
    );
    """)


def criar_estoque(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id_estoque SERIAL PRIMARY KEY,
        id_produto INT,
        id_loja INT,
        quantidade_atual INT,
        quantidade_minima INT,
        quantidade_maxima INT,
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
        FOREIGN KEY (id_loja) REFERENCES loja(id_loja),
        UNIQUE (id_produto, id_loja)
    );
    """)


def popular_banco():
    conn = conectar()
    with conn:
        with conn.cursor() as cur:
            # Tabelas que não têm dependências
            criar_categoria(cur)
            criar_fornecedor(cur)
            criar_loja(cur)
            criar_cliente(cur)

            # Produto (tem FK em categoria)
            criar_produto(cur)

            # Relacionamento produto <-> fornecedor
            criar_produto_fornecedor(cur)

            # Funcionário (tem FK em loja)
            criar_funcionario(cur)
            

            # Venda e seus itens
            criar_venda(cur)
            criar_item_venda(cur)

            # Compra e seus itens
            criar_compra(cur)
            criar_item_compra(cur)

            # Avaliação e promoção
            criar_avaliacao(cur)
            criar_promocao(cur)
            criar_produto_promocao(cur)

            # Estoque (produto + loja)
            criar_estoque(cur)
    conn.close()




def inserir_produto(prod):
    conn = conectar()
    sql = """
      INSERT INTO produto (nome, categoria, marca, preco, estoque)
      VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (prod.nome, prod.categoria, prod.marca, prod.preco, prod.estoque))
            pid = cur.fetchone()[0]
    conn.close()
    return pid

# Registrar venda
def registrar_venda(pid, qtd, total, data_hora, cidade, estado, pais):
    conn = conectar()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO dim_tempo (
                  data_hora, ano, mes, dia, hora, minuto, segundo, trimestre
                )
                VALUES (
                  %s,
                  EXTRACT(YEAR FROM %s::timestamp),
                  EXTRACT(MONTH FROM %s::timestamp),
                  EXTRACT(DAY FROM %s::timestamp),
                  EXTRACT(HOUR FROM %s::timestamp),
                  EXTRACT(MINUTE FROM %s::timestamp),
                  EXTRACT(SECOND FROM %s::timestamp),
                  EXTRACT(QUARTER FROM %s::timestamp)
                )
                ON CONFLICT (data_hora) DO NOTHING
                """,
                (data_hora, data_hora, data_hora, data_hora, data_hora, data_hora, data_hora, data_hora)
            )

            cur.execute(
                """
                INSERT INTO dim_local (cidade, estado, pais)
                VALUES (%s, %s, %s)
                ON CONFLICT (cidade, estado, pais) DO NOTHING
                """,
                (cidade, estado, pais),
            )

            cur.execute(
                """
                SELECT id FROM dim_local
                WHERE cidade = %s AND estado = %s AND pais = %s
                """,
                (cidade, estado, pais),
            )
            id_local = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO fato_venda (
                  data_hora, produto_id, quantidade, valor_total, local_id,
                  data_criacao, data_atualizacao
                )
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (data_hora, pid, qtd, total, id_local),
            )
    conn.close()

# Consulta de vendas por hora
def fetch_vendas_por_hora():
    conn = conectar()
    sql = """
      SELECT
        ano, mes, dia, hora,
        SUM(valor_total) AS total_vendas
      FROM fato_venda
      JOIN dim_tempo USING(data_hora)
      GROUP BY ano, mes, dia, hora
      ORDER BY ano, mes, dia, hora;
    """
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    conn.close()
    return rows

def get_dados_para_previsao():
    conn = conectar()
    sql = """
        SELECT
            dt.ano,
            dt.mes,
            dt.dia,
            SUM(fv.valor_total) AS total_vendas
        FROM fato_venda fv
        JOIN dim_tempo dt ON fv.id_tempo = dt.id_tempo
        GROUP BY dt.ano, dt.mes, dt.dia
        ORDER BY dt.ano, dt.mes, dt.dia;
    """
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    conn.close()
    return rows

def fetch_olap_vendas_completo():
    conn = conectar()
    sql = """
        SELECT 
            dt.ano,
            dt.mes,
            dt.dia,
            lj.nome_loja,
            dp.nome_produto,
            dc.nome_categoria AS categoria,
            dp.marca,
            SUM(fv.valor_total) AS total_vendas
        FROM fato_venda fv
        JOIN dim_tempo dt ON fv.id_tempo = dt.id_tempo
        JOIN loja lj ON fv.id_loja = lj.id_loja
        JOIN dim_produto dp ON fv.id_produto = dp.id_produto
        JOIN dim_categoria dc ON dp.id_categoria = dc.id_categoria
        GROUP BY dt.ano, dt.mes, dt.dia, lj.nome_loja, dp.nome_produto, dc.nome_categoria, dp.marca
        ORDER BY dt.ano, dt.mes, dt.dia;
    """
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    conn.close()
    return rows

# 📈 Previsão de vendas
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def prever_vendas():
    """
    Usa regressão linear simples para prever vendas com base no tempo (hora sequencial).
    """
    dados = get_dados_para_previsao()
    if not dados:
        print("⚠️ Nenhum dado encontrado para previsão.")
        return

    df = pd.DataFrame(dados)
    df["tempo"] = np.arange(len(df))  # tempo como sequência
    X = df[["tempo"]]
    y = df["total_vendas"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    futuro_tempo = np.arange(len(df), len(df) + 5).reshape(-1, 1)
    previsoes = modelo.predict(futuro_tempo)

    print("📊 Previsões para os próximos 5 períodos:")
    for i, p in enumerate(previsoes):
        print(f"Período +{i+1}: R$ {p:.2f}")

    # Exibir gráfico
    plt.plot(df["tempo"], y, label="Histórico")
    plt.plot(futuro_tempo, previsoes, label="Previsão", linestyle="--")
    plt.xlabel("Tempo (período)")
    plt.ylabel("Total de Vendas")
    plt.legend()
    plt.title("Previsão de Vendas (Regressão Linear)")
    plt.grid(True)
    plt.show()
    
    
def consulta_olap():
    conn = conectar()
    sql = """
    SELECT
        dt.ano,
        dt.mes,
        l.estado,
        l.cidade,
        dc.nome_categoria AS categoria,
        dp.marca,
        SUM(fv.quantidade) AS total_quantidade,
        SUM(fv.valor_total) AS total_valor
    FROM fato_venda fv
    JOIN dim_tempo dt ON fv.id_tempo = dt.id_tempo
    JOIN loja l ON fv.id_loja = l.id_loja
    JOIN dim_produto dp ON fv.id_produto = dp.id_produto
    JOIN dim_categoria dc ON dp.id_categoria = dc.id_categoria
    GROUP BY
        dt.ano, dt.mes,
        l.estado, l.cidade,
        dc.nome_categoria,
        dp.marca
    ORDER BY dt.ano, dt.mes;
    """
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            resultado = cur.fetchall()
    conn.close()  # fechar conexão antes do retorno

    # Exibir no terminal como tabela
    df = pd.DataFrame(resultado)
    print("\n📊 RESULTADO OLAP:\n")
    print(df)
    print("faz o L porraaaaaaa")
    return df


def consulta_olap_dinamica(agrupamentos=[], filtros={}):
    conn = conectar()

    dimensoes = {
        "ano": "dt.ano",
        "mes": "dt.mes",
        "dia": "dt.dia",
        "categoria": "p.categoria",  # Aqui, categoria é id_categoria? Talvez precise ajustar
        "marca": "p.marca"
    }

    select_cols = []
    group_by_cols = []

    for ag in agrupamentos:
        if ag in dimensoes:
            select_cols.append(dimensoes[ag])
            group_by_cols.append(dimensoes[ag])

    select_clause = ", ".join(select_cols) if select_cols else ""
    group_by_clause = ", ".join(group_by_cols) if group_by_cols else ""

    sql = f"""
        SELECT
            {select_clause}{"," if select_clause else ""}
            SUM(fv.quantidade) AS total_quantidade,
            SUM(fv.valor_total) AS total_valor
        FROM fato_venda fv
        JOIN dim_tempo dt ON fv.id_tempo = dt.id_tempo
        JOIN produto p ON fv.id_produto = p.id_produto
        WHERE 'SP' = 'SP'
    """

    where_conditions = []
    values = []
    if filtros:
        for key, value in filtros.items():
            if key in dimensoes:
                where_conditions.append(f"{dimensoes[key]} = %s")
                values.append(value)

    if where_conditions:
        sql += " AND " + " AND ".join(where_conditions)

    if group_by_clause:
        sql += f" GROUP BY {group_by_clause} ORDER BY {group_by_clause};"
    else:
        sql += ";"

    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, tuple(values))
            resultado = cur.fetchall()

    conn.close()

    df = pd.DataFrame(resultado)
    print("\n📊 RESULTADO OLAP DINÂMICO:\n")
    print(df)
    return df

def listar_produtos_postgres(conexao):
    try:
        cursor = conexao.cursor()

        query = "SELECT * FROM produtos;"
        cursor.execute(query)

        produtos = cursor.fetchall()

        print("\n--- Lista de Produtos ---")
        for produto in produtos:
            print(produto)

        cursor.close()

    except Exception as e:
        print(f"Erro ao listar produtos: {e}")


# Execução direta
if __name__ == "__main__":
    print("▶️ Rodando script com previsão de vendas...")
    popular_banco()
    

#funciona pelo amor de deus
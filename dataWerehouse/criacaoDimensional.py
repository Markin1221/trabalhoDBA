import psycopg2
from config import POSTGRES

# Conectar ao banco
def conectar():
    conn = psycopg2.connect(**POSTGRES)
    print("🔌 Conectado ao banco:", conn.get_dsn_parameters()["dbname"])
    return conn

def criar_dim_categoria(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_categoria (
            id_categoria INT PRIMARY KEY,
            nome_categoria VARCHAR(50),
            descricao TEXT
        );
    """)

def criar_dim_tempo(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_tempo (
        id_tempo SERIAL PRIMARY KEY,
        data DATE UNIQUE,
        ano INT,
        semestre INT,
        trimestre INT,
        mes INT,
        nome_mes VARCHAR(20),
        dia INT,
        nome_dia_semana VARCHAR(20)
    );
    """)

def criar_dim_produto(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_produto (
        id_produto INT PRIMARY KEY,
        nome_produto VARCHAR(100),
        categoria VARCHAR(50),
        marca VARCHAR(50)
    );
    """)

def criar_dim_loja(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_loja (
        id_loja INT PRIMARY KEY,
        nome_loja VARCHAR(50),
        cidade VARCHAR(50),
        estado CHAR(2)
    );
    """)

def criar_dim_cliente(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_cliente (
        id_cliente INT PRIMARY KEY,
        nome_cliente VARCHAR(100),
        cidade VARCHAR(50),
        estado CHAR(2)
    );
    """)

def criar_fato_venda(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fato_venda (
        id_fato SERIAL PRIMARY KEY,
        id_tempo INT,
        id_produto INT,
        id_loja INT,
        id_cliente INT,
        quantidade INT,
        valor_total DECIMAL(10,2),
        desconto DECIMAL(10,2),
        FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
        FOREIGN KEY (id_produto) REFERENCES dim_produto(id_produto),
        FOREIGN KEY (id_loja) REFERENCES dim_loja(id_loja),
        FOREIGN KEY (id_cliente) REFERENCES dim_cliente(id_cliente)
    );
    """)

def criar_tabelas_dw():
    try:
        conn = conectar()
        cur = conn.cursor()

        criar_dim_tempo(cur)
        criar_dim_produto(cur)
        criar_dim_loja(cur)
        criar_dim_cliente(cur)
        criar_fato_venda(cur)

        conn.commit()
        print("Tabelas do Data Warehouse criadas com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    criar_tabelas_dw()

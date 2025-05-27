from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from config import POSTGRES
import pandas as pd

def conectar():
    conn = psycopg2.connect(**POSTGRES)
    print("🔌 Conectado ao banco:", conn.get_dsn_parameters()["dbname"])
    return conn

def popular_tabelas_mais_exemplos():
    conn = conectar()

    with conn:
        with conn.cursor() as cur:
            # Limpa tabelas para evitar conflito de FK
            cur.execute("TRUNCATE TABLE fato_venda RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE dim_produto RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE dim_tempo RESTART IDENTITY CASCADE;")

            # Popula dim_tempo com id_tempo fixo (1 a 20)
            datas = [(i, 2024, 1, i) for i in range(1, 21)]
            for id_tempo, ano, mes, dia in datas:
                cur.execute("""
                    INSERT INTO dim_tempo (id_tempo, ano, mes, dia)
                    VALUES (%s, %s, %s, %s)
                """, (id_tempo, ano, mes, dia))

            # Popula dim_produto com id_produto fixo (1 a 20) com nomes e marcas reais
            produtos = [
                (1, "COD001", "Notebook Dell XPS 13", 1, "Dell", 7500.00),
                (2, "COD002", "Smartphone Apple iPhone 13", 2, "Apple", 6000.00),
                (3, "COD003", "Câmera Canon EOS R5", 3, "Canon", 15000.00),
                (4, "COD004", "Tablet Samsung Galaxy Tab S7", 1, "Samsung", 3500.00),
                (5, "COD005", "Fone de Ouvido Bose QuietComfort 35", 2, "Bose", 1200.00),
                (6, "COD006", "Smartwatch Apple Watch Series 7", 3, "Apple", 3200.00),
                (7, "COD007", "Monitor LG UltraFine 27''", 1, "LG", 2600.00),
                (8, "COD008", "Teclado Mecânico Logitech G Pro", 2, "Logitech", 900.00),
                (9, "COD009", "Mouse Gamer Razer DeathAdder", 3, "Razer", 400.00),
                (10, "COD010", "Impressora HP LaserJet Pro", 1, "HP", 1800.00),
                (11, "COD011", "Headset Microsoft Surface", 2, "Microsoft", 1300.00),
                (12, "COD012", "Webcam Logitech C920", 3, "Logitech", 500.00),
                (13, "COD013", "Caixa de Som JBL Flip 5", 1, "JBL", 700.00),
                (14, "COD014", "SSD Samsung 1TB EVO Plus", 2, "Samsung", 900.00),
                (15, "COD015", "Placa de Vídeo Nvidia RTX 3080", 3, "Nvidia", 8500.00),
                (16, "COD016", "Smartphone Xiaomi Mi 11", 1, "Xiaomi", 2800.00),
                (17, "COD017", "Tablet Apple iPad Air", 2, "Apple", 4500.00),
                (18, "COD018", "Notebook Asus ZenBook 14", 3, "Asus", 6800.00),
                (19, "COD019", "Câmera Sony Alpha a7 III", 1, "Sony", 12000.00),
                (20, "COD020", "Monitor Dell UltraSharp 24''", 2, "Dell", 2200.00)
            ]
            for id_produto, codigo, nome, id_categoria, marca, preco in produtos:
                cur.execute("""
                    INSERT INTO dim_produto (id_produto, codigo, nome_produto, id_categoria, marca, preco_atual)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_produto, codigo, nome, id_categoria, marca, preco))

            # Popula fato_venda com dados fixos, referenciando as FK corretas
            vendas = []
            id_fato = 1
            for id_tempo in range(1, 21):
                # Vende 2 produtos diferentes por dia
                for id_produto in [id_tempo, (id_tempo % 20) + 1]:
                    valor_total = 20.0 + (id_produto * 5)
                    quantidade = int(valor_total // 10)
                    vendas.append((id_fato, id_tempo, id_produto, quantidade, valor_total))
                    id_fato += 1

            for id_fato, id_tempo, id_produto, quantidade, valor_total in vendas:
                cur.execute("""
                    INSERT INTO fato_venda (id_fato, id_tempo, id_produto, quantidade, valor_total)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_fato, id_tempo, id_produto, quantidade, valor_total))

    conn.close()
    print("✅ Tabelas populadas com mais exemplos para OLAP.")

if __name__ == "__main__":
    popular_tabelas_mais_exemplos()

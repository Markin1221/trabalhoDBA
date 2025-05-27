import psycopg2
from datetime import date
from config import POSTGRES

# Conectar ao banco
def conectar():
    conn = psycopg2.connect(**POSTGRES)
    print("🔌 Conectado ao banco:", conn.get_dsn_parameters()["dbname"])
    return conn




def popular_dim_categoria(cur):
    categorias = [
        (1, 'Eletrônicos', 'Produtos eletrônicos como celulares, TVs, computadores'),
        (2, 'Alimentos', 'Produtos alimentícios e bebidas'),
        (3, 'Roupas', 'Vestuário masculino, feminino e infantil'),
        (4, 'Calçados', 'Sapatos, tênis e sandálias'),
        (5, 'Móveis', 'Móveis para casa e escritório'),
        (6, 'Esportes', 'Equipamentos e roupas esportivas'),
        (7, 'Beleza', 'Produtos de beleza e higiene pessoal'),
        (8, 'Livros', 'Livros de todos os gêneros e tipos'),
        (9, 'Brinquedos', 'Brinquedos e jogos para crianças'),
        (10, 'Automotivo', 'Peças e acessórios para veículos')
    ]

    for categoria in categorias:
        cur.execute("""
            INSERT INTO dim_categoria (id_categoria, nome_categoria, descricao)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_categoria) DO NOTHING;
        """, categoria)

if __name__ == "__main__":
    conn = conectar()
    cur = conn.cursor()

    try:
        popular_dim_categoria(cur)
        conn.commit()
        print("✅ Tabela dim_categoria populada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao popular a tabela dim_categoria: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
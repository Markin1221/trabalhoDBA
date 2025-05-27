def atualizar_categoria_produtos(cur):
    atualizacoes = [
        (1, 'Smartphone XYZ'),
        (2, 'Camiseta Azul'),
        (3, 'Livro Python Avançado'),
        (4, 'Chocolate 70%'),
        (5, 'Cadeira Gamer')
    ]
    cur.executemany("""
        UPDATE dim_produto
        SET id_categoria = %s
        WHERE LOWER(nome_produto) = LOWER(%s);
    """, atualizacoes)
    print(f"Linhas atualizadas: {cur.rowcount}")

if __name__ == "__main__":
    from config import POSTGRES
    import psycopg2

    conn = psycopg2.connect(**POSTGRES)
    cur = conn.cursor()

    try:
        atualizar_categoria_produtos(cur)
        conn.commit()
        print("Categorias atualizadas com sucesso.")
    except Exception as e:
        print("Erro:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

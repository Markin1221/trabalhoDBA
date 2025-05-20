from persistent import Persistent

class Categoria(Persistent):
    def __init__(self, nome):
        self.nome = nome

class Produto(Persistent):
    def __init__(self, nome, descricao, preco, categoria):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
    def printar(self):
        print(f"Produto: {self.nome}, Descrição: {self.descricao}, Preço: {self.preco}, Categoria: {self.categoria.nome}")
        


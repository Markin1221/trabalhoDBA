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
        print(f"{self.nome} | {self.descricao} | R${self.preco:.2f} | Categoria: {self.categoria.nome}")

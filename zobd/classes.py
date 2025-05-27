from persistent import Persistent
from persistent.list import PersistentList

class Categoria(Persistent):
    def __init__(self, id_categoria, nome_categoria, descricao=None):
        self.id_categoria = id_categoria
        self.nome_categoria = nome_categoria
        self.descricao = descricao
        self.produtos = PersistentList()  

class Produto(Persistent):
    def __init__(self, id_produto, codigo_produto, nome_produto, descricao, preco_atual, categoria, marca, unidade_medida, ativo=True):
        self.id_produto = id_produto
        self.codigo_produto = codigo_produto
        self.nome_produto = nome_produto
        self.descricao = descricao
        self.preco_atual = preco_atual
        self.categoria = categoria  
        self.marca = marca
        self.unidade_medida = unidade_medida
        self.ativo = ativo
        self.fornecedores = []
        categoria.produtos.append(self)
        
class Fornecedor(Persistent):
    def __init__(self, cnpj, razao_social, nome_fantasia, telefone, email, endereco, cidade, estado, ativo=True):
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.produtos = []
        self.ativo = ativo
        self.produtos = PersistentList()

class ProdutoFornecedor(Persistent):
    def __init__(self, produto, fornecedor, preco_compra, prazo_entrega):
        self.produto = produto
        self.fornecedor = fornecedor
        self.preco_compra = preco_compra
        self.prazo_entrega = prazo_entrega

        produto.fornecedores.append(self)
        fornecedor.produtos.append(self)

class Estoque(Persistent):
    def __init__(self, produto, loja, quantidade_atual, quantidade_minima, quantidade_maxima):
        self.produto = produto
        self.loja = loja
        self.quantidade_atual = quantidade_atual
        self.quantidade_minima = quantidade_minima
        self.quantidade_maxima = quantidade_maxima

class Promocao(Persistent):
    def __init__(self, nome_promocao, descricao, data_inicio, data_fim, percentual_desconto, ativa=True):
        self.nome_promocao = nome_promocao
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.percentual_desconto = percentual_desconto
        self.ativa = ativa
        self.produtos = PersistentList()

class ProdutoPromocao(Persistent):
    def __init__(self, produto, promocao, preco_promocional):
        self.produto = produto
        self.promocao = promocao
        self.preco_promocional = preco_promocional

        promocao.produtos.append(self)

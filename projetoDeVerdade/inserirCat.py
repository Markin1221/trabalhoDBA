from ZODB import FileStorage, DB
import transaction
import ZODB
import ZODB.DB
from persistent import Persistent
from persistent.list import PersistentList
import ZODB.FileStorage

# Importando suas classes
from classes import Categoria  # Altere 'suas_classes' para o nome do seu arquivo Python se necessário

# 🗂️ Abrindo conexão com o banco ZODB
storage = FileStorage.FileStorage('banco.fs')
db = DB(storage)
connection = db.open()
root = connection.root


# ✅ Criando objetos Categoria
cat1 = Categoria(id_categoria=1, nome_categoria="Eletrônicos", descricao="Produtos eletrônicos em geral")
cat2 = Categoria(id_categoria=2, nome_categoria="Alimentos", descricao="Produtos alimentícios")
cat3 = Categoria(id_categoria=3, nome_categoria="Vestuário", descricao="Roupas, calçados e acessórios")
cat4 = Categoria(id_categoria=4, nome_categoria="Papelaria", descricao="Itens de papelaria e escritório")

# 💾 Inserindo no banco
root['categorias'].extend([cat1, cat2, cat3, cat4])

# 💡 Confirmando a transação
transaction.commit()

print("Categorias inseridas com sucesso!")

# 🔐 Fechando conexão
connection.close()
db.close()

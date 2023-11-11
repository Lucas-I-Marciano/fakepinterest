# Criar estrutura do Banco de Dados

from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario) :
    return Usuario.query.get(int(id_usuario)) # Retorna um usuário pela PrimaryKey


class Usuario(database.Model, UserMixin) : # Basicamente passo esse parâmetro para o banco de dados entender que estou criando uma tabela
    id = database.Column(database.Integer, primary_key=True, )
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique=True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True) # 1º Argumento é a classe que se refere ; "usuario" é como se fosse uma coluna a mais na tablea Foto para relacionar, mas só passa aqui para ficar mais fácil ; Lazy é legal passar quando tem relação para otimizar


class Foto(database.Model) :
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default = "default.png")
    data_criacao = database.Column(database.DateTime, nullable = False, default = datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable = False) # No ForeignKey eu passo [nomeTabela].[colunaPrimaria]

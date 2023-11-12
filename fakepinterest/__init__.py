from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db" # Para criar um banco de dados local
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://banco_fakepinterest_oog2_user:qUPevYWvReuAlssZhsYy0f3UPkbJFvvE@dpg-cl8j2oqvokcc73b0bdf0-a.oregon-postgres.render.com/banco_fakepinterest_oog2" # Criar o banco a primeira vez no ambiente do render
app.config['SECRET_KEY'] = '9ff474c43a225a9896224156a89a4700' # secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/fotos_post'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'homepage' # Nome da função que direciona o usuário para a página

from fakepinterest import routes
from fakepinterest import app, database
from fakepinterest.models import Usuario, Foto

with app.app_context() : # Exigência recente para criar banco de dados "Criar dentro de um Contexto"
    database.create_all()

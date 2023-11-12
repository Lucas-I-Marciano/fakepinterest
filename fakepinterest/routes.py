# Criar as rotas do Site (Links)

from flask import render_template # Procura a pasta "templates" e deixar maix fácil importar esses arquivos HTML
from flask import url_for # Faz o link entre página ficar dinâmico (linkar com o nome da função e não com o nome da página) - Que é esperado mudar menos
from fakepinterest import app, database, bcrypt
from flask_login import login_required # Exigir que um usuário tenha login para acessar páginas
from fakepinterest.forms import FormCriarConta, FormLogin # Para eu passar como parâmetro e usar na á página HTML
from fakepinterest.models import Usuario, Foto # Para validar a criação de um usuário
from flask import redirect # Redirecionar para páginas específicas
from flask_login import login_user, logout_user # Depois de direcionar ele precisa estar logado
from flask_login import current_user
from fakepinterest.forms import FormFoto # Caso eu esteja o Usuário atual esteja no perfil, vou deixar ele importat uma foto
import os
from werkzeug.utils import secure_filename

@app.route("/", methods = ['GET', 'POST']) # Porque vou ter um formulário 'POST'
def homepage() :
    form_login = FormLogin()
    if form_login.validate_on_submit() :
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data) : # Comparo a senha criptografada com a não criptografada (A do BD com a Preenchida)
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario = usuario.id))
    return render_template("homepage.html", form = FormLogin())
    # return render_template("homepage.html", form = FormLogin(), teste = database.session.query(Usuario).first().username, teste2=Usuario.query.filter_by(email='lucas@gmail.com').first().username)

@app.route('/criar-conta', methods = ['GET', 'POST'])
def criarconta ():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() :
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) # Para trazer proteção e criptografar a senha
        usuario = Usuario(username = form_criarconta.username.data, 
                        email = form_criarconta.email.data, 
                        senha = senha) # Vou criar meu usuário no banco de dados
        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember = True)
        return redirect(url_for('perfil', id_usuario = usuario.id))
    
    return render_template('criarconta.html', form = FormCriarConta())

@app.route('/perfil/<id_usuario>', methods=['GET', 'POST']) # "<" e ">" indica que estou inserindo uma variável
@login_required
def perfil(id_usuario) : # A função deve receber a mesma variável
    teste = app.config['UPLOAD_FOLDER']
    if int(id_usuario) == int(current_user.id) : # Conferindo se o usuário que vou mostrar o perfil é o usuário atual
        form_foto = FormFoto()
        if form_foto.validate_on_submit() :
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename) # Tirar caracteres que podem quebrar o código

            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                        app.config['UPLOAD_FOLDER'], nome_seguro)
            teste = caminho
            arquivo.save(caminho) # Salvar o nome da imagem no Banco de dados (Não salvar a imagem em si para não ficar um banco de dados gigante)

            foto = Foto(imagem = nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', usuario = current_user, form = form_foto, teste = teste)
    else :
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario = usuario, form = None, teste = teste)

@app.route('/logout')
@login_required
def logout() :
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
def feed() :
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all() # Lista de tudo que eu tenho no Banco de Dados
    return render_template('feed.html', fotos = fotos)
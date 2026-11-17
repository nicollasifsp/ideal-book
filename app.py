from flask import *
from flask_sqlalchemy import *
from database.db import db
from model.usuarioModel import UsuarioModel
from model.colecaoModel import ColecaoModel
from model.progressoModel import ProgressoModel
from controller.controllerUsuario import ControllerUsuario
from controller.controllerLivro import ControllerLivro
from controller.controllerCapitulo import ControllerCapitulo
from controller.controllerColecao import ControllerColecao
import os
from werkzeug.utils import secure_filename
import uuid
from dotenv import *
from datetime import timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, get_jwt,
    verify_jwt_in_request,
    set_access_cookies, unset_jwt_cookies
)


controllerUsuario=ControllerUsuario()
controllerLivro=ControllerLivro()
controllerCapitulo=ControllerCapitulo()
controllerColecao=ControllerColecao()


app=Flask(__name__)

app.config["JWT_SECRET_KEY"] = "troque-esta-chave-em-producao"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

# Permite que o JWT seja lido a partir de Cookies enviados pelo navegador
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///idealBook.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

STATIC_FOLDER = "static"
IMG_FOLDER = os.path.join(STATIC_FOLDER,"img")
JS_FOLDER = os.path.join(STATIC_FOLDER, "js")
CSS_FOLDER = os.path.join(STATIC_FOLDER, "css")

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

os.makedirs(IMG_FOLDER, exist_ok=True)
os.makedirs(JS_FOLDER, exist_ok=True)
os.makedirs(CSS_FOLDER, exist_ok=True)


#LOGIN OBRIGATORIO:
def login_obrigatorio(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return redirect(url_for("renderLogin"))

        return view(*args, **kwargs)

    return wrapper


@app.context_processor
def injetar_usuario():
    usuario_atual = None
    try:
        verify_jwt_in_request(optional=True)
        identidade = get_jwt_identity()
        if identidade:
            usuario_atual = controllerUsuario.getUserId(int(identidade))
    except Exception:
        usuario_atual = None

    def url_capa(caminho):
        if not caminho:
            return ""
        normalizado = caminho.replace("\\", "/")
        if normalizado.startswith(("http://", "https://", "/")):
            return normalizado
        return "/" + normalizado

    return dict(usuario_atual=usuario_atual, url_capa=url_capa)

# LOGIN OBRIGATORIO TIPO DE USUARIO:
def tipo_usuario_obrigatorio(tipo):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):

            try:
                verify_jwt_in_request()
            except Exception:
                return redirect(url_for("renderLogin"))

            usuario = get_jwt()

            if usuario.get("tipoUsuario") != tipo:
                abort(403)

            return view(*args, **kwargs)

        return wrapper
    return decorator

#os renders
@app.route("/")
def home():
    livros = controllerLivro.getLivros()[:8]
    favoritos_ids = set()
    try:
        verify_jwt_in_request(optional=True)
        identidade = get_jwt_identity()
        if identidade:
            favoritos_ids = controllerColecao.getIdsColecao(int(identidade))
    except Exception:
        pass
    return render_template('index.html', livros=livros, favoritos_ids=favoritos_ids)
@app.route("/renderLogin")
def renderLogin():
    return render_template("login.html")

@app.route("/renderCadastro")
def renderCadastro():
    return render_template("cadastro.html")

@app.route("/cadastrarLivro")
@tipo_usuario_obrigatorio("escritor")
def renderCadastrarLivro():
    return render_template("cadastrarLivro.html")

@app.route("/Login", methods=["POST"])
def fazerLogin():
    email = request.form["email"]
    senha = request.form["senha"]

    mensagemLogin = controllerUsuario.fazerLogin(email, senha)

    if mensagemLogin == False:
        return render_template(
            "login.html",
            erro="Usuário não encontrado, tente criar uma conta"
        )

    token = create_access_token(
        identity=str(mensagemLogin.id),
        additional_claims={
            "tipoUsuario": mensagemLogin.tipoUsuario
        }
    )

    if mensagemLogin.tipoUsuario == "leitor":
        resposta = redirect(url_for("biblioteca"))
    else:
        resposta = redirect(url_for("renderCadastrarLivro"))

    set_access_cookies(resposta, token)

    return resposta
        

@app.route('/Cadastro',methods=["POST"])
def fazerCadastro():
    nome=request.form["nome"]
    email=request.form["email"]
    senha=request.form["senha"]
    confirmarSenha=request.form["confirmarSenha"]
    tipoUsuario=request.form["tipoUsuario"].lower()
    if senha==confirmarSenha:
        mensagem=controllerUsuario.salvarUsuario(nome,email,senha,tipoUsuario)
    else:
        return render_template("cadastro.html",erro="Verifique se as duas senhas estão corretas")
    
    if mensagem ==True:
        return render_template("login.html")
    else:
        return render_template("cadastro.html",erro="Esse usuário já foi cadastrado")
    
@app.route("/cadastrarLivro",methods=["POST"])
@tipo_usuario_obrigatorio("escritor")
def cadastrarLivro():
    titulo=request.form["titulo"]
    autor=request.form["autor"]
    descricao=request.form["descricao"]
    
    imagem=request.files["imagem"]

    if imagem and imagem.filename != "":

        # pega extensão do arquivo
        ext = imagem.filename.split(".")[-1]

        # cria nome único
        imagemNome = f"{uuid.uuid4()}.{ext}"

        # monta caminho correto
        caminhoImagem = os.path.join(IMG_FOLDER, imagemNome)
        print("esse é o caminho da imagem: ",caminhoImagem)

        # salva
        imagem.save(caminhoImagem)
    idUsuario=int(get_jwt_identity())

    mensagem=controllerLivro.salvarLivro(titulo,autor,descricao,caminhoImagem,idUsuario)
    if mensagem==True:
        return render_template("cadastrarLivro.html",sucesso="Livro adicionado com sucesso.")
    else:
        return render_template("cadastrarLivro.html",erro="infezmente occoreu um erro, tente novamante")

@app.route("/biblioteca")
@login_obrigatorio
def biblioteca():
    busca = request.args.get("q", "").strip()
    livros = controllerLivro.getLivros()
    if busca:
        termo = busca.lower()
        livros = [
            l for l in livros
            if termo in l.titulo.lower() or termo in l.autor.lower()
        ]
    idUsuario = int(get_jwt_identity())
    favoritos_ids = controllerColecao.getIdsColecao(idUsuario)
    return render_template("biblioteca.html", livros=livros, favoritos_ids=favoritos_ids, busca=busca)

@app.route("/favoritos")
@login_obrigatorio
def favoritos():
    idUsuario = int(get_jwt_identity())
    livros = controllerColecao.getLivrosColecao(idUsuario)
    favoritos_ids = {l.id for l in livros}
    return render_template("favoritos.html", livros=livros, favoritos_ids=favoritos_ids)

@app.route("/favoritar/<int:idLivro>", methods=["POST"])
@app.route("/favoritar/livro/<int:idLivro>", methods=["GET", "POST"])
@login_obrigatorio
def favoritar(idLivro):
    idUsuario = int(get_jwt_identity())
    livro = controllerLivro.getLivroIdLivro(idLivro)
    if not livro:
        abort(404)

    status = controllerColecao.favoritarLivro(idUsuario, idLivro)
    if status is None:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
            return jsonify({"erro": "Erro ao atualizar favorito"}), 500
        return redirect(request.referrer or url_for("biblioteca"))

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"favorito": status, "idLivro": idLivro})

    return redirect(request.referrer or url_for("biblioteca"))

@app.route("/lerLivro/<id>")
@login_obrigatorio
def lerLivro(id):
    idLivro=int(id)
    idUsuario=int(get_jwt_identity())
    livro=controllerLivro.getLivroIdLivro(idLivro)
    capitulos=controllerCapitulo.getCapitulos(idLivro)
    is_favorito=controllerColecao.isFavorito(idUsuario, idLivro)
    return render_template("lerLivro.html",capitulos=capitulos,livro=livro,is_favorito=is_favorito)

@app.route("/lerCapitulo/<int:idCapitulo>")
@login_obrigatorio
def lerCapitulo(idCapitulo):
    capitulo=controllerCapitulo.getCapitulo(idCapitulo)
    return render_template("lerCapitulo.html",capitulo=capitulo)

    

@app.route("/obras")
@login_obrigatorio
def obras():
    idUsuario=int(get_jwt_identity())
    livros=controllerLivro.getLivrosAutor(idUsuario)
    
    return render_template("obras.html",livros=livros)

@app.route("/obras/<int:idLivro>")
@login_obrigatorio
def menuLivro(idLivro):
    livro=controllerLivro.getLivroIdLivro(idLivro)
    idSession=int(get_jwt_identity())
    if not livro:
        abort(404)
        return
    if livro.idUsuario==idSession:
        capitulos=controllerCapitulo.getCapitulos(livro.id)
        return render_template("menuLivro.html",capitulos=capitulos,livro=livro)
    else:
        abort(403)
        return

@app.route("/obras/adicionar/<int:idLivro>",methods=["POST","GET"])
@tipo_usuario_obrigatorio("escritor")
def addCapitulo(idLivro):
    livro=controllerLivro.getLivroIdLivro(idLivro)
    if request.method=="GET":
        return render_template("addCapitulo.html", livro=livro)
    else:
        titulo=request.form["titulo"]
        conteudo=request.form["conteudo"]
        mensagem=controllerCapitulo.salvarCapitulo(titulo,conteudo,idLivro)
        
        if mensagem==True:
            return render_template("addCapitulo.html",sucesso="Capítulo addiconado com sucesso.",livro=livro)
        else:
            return render_template("addCapitulo.html",erro="infelizmente occoreu um erro, tente novamente mais tarde.",livro=livro)

@app.route("/obras/editar/<int:idCapitulo>",methods=["GET","POST"])
@tipo_usuario_obrigatorio("escritor")
def editarCapitulo(idCapitulo):
    
    capitulo=controllerCapitulo.getCapitulo(idCapitulo)
    if request.method=="GET":
        return render_template("editarCapitulo.html",capitulo=capitulo)
    else:
        titulo=request.form["titulo"]
        conteudo=request.form["conteudo"]
        mensagem=controllerCapitulo.updateCapitulo(idCapitulo,titulo,conteudo)
        if mensagem==True:
            return render_template("editarCapitulo.html",sucesso="Capítulo atualizado com sucesso",capitulo=capitulo)
        else:
            return render_template("editarCapitulo.html",erro="infelizmente ocorreu um erro tente mais tarde",capitulo=capitulo)
        
    


@app.route("/deletar/capitulo/<int:idCapitulo>")
@tipo_usuario_obrigatorio("escritor")
def deletarCapituloId(idCapitulo):
    #será que preciso fazer a validação para ver se o livro realmente pertence ao usuário?
    capitulo=controllerCapitulo.getCapitulo(idCapitulo)

    if not capitulo:
        abort(400)
        return 
    idLivro=capitulo.idLivro

    if not idLivro:
        return abort(404)
    
    livro=controllerLivro.getLivroIdLivro(idLivro)
    print(f"O ID DO LIVRO É: {idLivro}")

    if not livro:
        abort(401)
        return
    
    idSession=int(get_jwt_identity())
    
    if idSession==livro.idUsuario:
        mensagem=controllerCapitulo.deletarCapituloId(capitulo)
        capitulos=controllerCapitulo.getCapitulos(idLivro)
    else:
        abort(401)
        return
    if mensagem == True:
        return render_template("menuLivro.html",sucessoDelete="capítulo deletado com sucesso",capitulos=capitulos,livro=livro)
    else:
        return render_template("menuLivro.html",erroDelete="erro ao deletar o capítulo",capitulos=capitulos,livro=livro)


@app.route("/deletar/livro/<int:idLivro>")
@tipo_usuario_obrigatorio("escritor")
def deleterLivroId(idLivro):
    livro = controllerLivro.getLivroIdLivro(idLivro)

    if not livro:
        abort(404)

    idSession = int(get_jwt_identity())

    if idSession != livro.idUsuario:
        abort(403)

    controllerColecao.deletarColecaoLivro(livro.id)
    mensagem = controllerLivro.deletarLivro(livro)
    livros=controllerLivro.getLivrosAutor(idSession)
    if mensagem == False:
        return render_template(
            "obras.html",
            erro="erro ao deletar o livro",
            livros=livros
        )

    mensagemCapitulo = controllerCapitulo.deletarCapitulos(livro.id)

    if mensagemCapitulo == False:
        return render_template(
            "obras.html",
            erro="erro ao deletar os capítulos",
            livros=livros
        )

    return redirect(
        url_for("obras",
        sucesso="livro e capítulos deletados com sucesso",
        livros=livros)

    )
    
# Logout    
@app.route("/logout")
def logout():
    resposta = redirect(url_for("renderLogin"))
    unset_jwt_cookies(resposta)
    return resposta


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
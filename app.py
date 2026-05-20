from flask import *
from flask_sqlalchemy import *
from database.db import db
from model.usuarioModel import UsuarioModel
from controller.controllerUsuario import ControllerUsuario
from controller.controllerLivro import ControllerLivro
import os
from werkzeug.utils import secure_filename
from dotenv import *


controllerUsuario=ControllerUsuario()
controllerLivro=ControllerLivro()


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///idealBook.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)
pasta="static"
app.config['UPLOAD_FOLDER'] = pasta
os.makedirs(pasta, exist_ok=True)

#os renders
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/renderLogin")
def renderLogin():
    return render_template("login.html")

@app.route("/renderCadastro")
def renderCadastro():
    return render_template("cadastro.html")

@app.route("/cadastrarLivro")
def renderCadastrarLivro():
    return render_template("cadastrarLivro.html")




@app.route("/Login",methods=["POST"])
def fazerLogin():
    email=request.form["email"]
    senha=request.form["senha"]
    mensagemLogin=controllerUsuario.fazerLogin(email,senha)
    if mensagemLogin==False:
        return render_template("login.html",erro="Usuário não encontrado, tente criar uma conta")
    else:
        session["user_id"] = mensagemLogin.id
        if mensagemLogin.tipoUsuario == "leitor":
            return redirect(url_for("biblioteca"))
        else:
            return redirect(url_for("renderCadastrarLivro"))

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
def cadastrarLivro():
    titulo=request.form["titulo"]
    autor=request.form["autor"]
    descricao=request.form["descricao"]
    
    quantPag=int(request.form["quantPag"])
    imagem=request.files["imagem"]

    imagemNome = secure_filename(imagem.filename)
    caminhoImagem = pasta + "/" + imagemNome
    imagem.save(caminhoImagem)
    idUsuario=session.get("user_id")

    mensagem=controllerLivro.salvarLivro(titulo,autor,descricao,caminhoImagem,quantPag,idUsuario)
    if mensagem==True:
        return render_template("cadastrarLivro.html",sucesso="Livro adicionado com sucesso.")
    else:
        return render_template("cadastrarLivro.html",erro="infezmente occoreu um erro, tente novamante")

@app.route("/biblioteca")
def biblioteca():
    livros=controllerLivro.getLivros()
    return render_template("biblioteca.html",livros=livros)

@app.route("/lerLivro/<id>")
def lerLivro(id):
    idLivo=int(id)
    livro=controllerLivro.getConteudo(id)
    return render_template("lerLivro.html",livro=livro)

@app.route("/obras")
def obras():
    idUsuario=session.get("user_id")
    livros=controllerLivro.getLivroAutor(idUsuario)
    controllerLivro.mostrarDados(livros)
    return render_template("obras.html",livros=livros)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
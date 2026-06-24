from flask import *
from flask_sqlalchemy import *
from database.db import db
from model.usuarioModel import UsuarioModel
from controller.controllerUsuario import ControllerUsuario
from controller.controllerLivro import ControllerLivro
from controller.controllerCapitulo import ControllerCapitulo
import os
from werkzeug.utils import secure_filename
from dotenv import *


controllerUsuario=ControllerUsuario()
controllerLivro=ControllerLivro()
controllerCapitulo=ControllerCapitulo()


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
    
    imagem=request.files["imagem"]

    imagemNome = secure_filename(imagem.filename)
    caminhoImagem = pasta + "/" + imagemNome
    imagem.save(caminhoImagem)
    idUsuario=session.get("user_id")

    mensagem=controllerLivro.salvarLivro(titulo,autor,descricao,caminhoImagem,idUsuario)
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
    idLivro=int(id)
    livro=controllerLivro.getLivroIdLivro(idLivro)
    capitulos=controllerCapitulo.getCapitulos(idLivro)
    return render_template("lerLivro.html",capitulos=capitulos,livro=livro)

@app.route("/lerCapitulo/<int:idCapitulo>")
def lerCapitulo(idCapitulo):
    capitulo=controllerCapitulo.getCapitulo(idCapitulo)
    return render_template("lerCapitulo.html",capitulo=capitulo)

    

@app.route("/obras")
def obras():
    idUsuario=session.get("user_id")
    livros=controllerLivro.getLivrosAutor(idUsuario)
    
    return render_template("obras.html",livros=livros)

@app.route("/obras/<int:idLivro>")
def menuLivro(idLivro):
    livro=controllerLivro.getLivroIdLivro(idLivro)
    idSession=session.get("user_id")
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
    
    idSession=session.get("user_id")
    
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
def deleterLivroId(idLivro):
    livro = controllerLivro.getLivroIdLivro(idLivro)

    if not livro:
        abort(404)

    idSession = session.get("user_id")

    if idSession != livro.idUsuario:
        abort(403)

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


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
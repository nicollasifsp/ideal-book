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
    idLivro=int(id)
    livro=controllerLivro.getLivroIdLivro(idLivro)
    capitulos=controllerCapitulo.getTodosCapitulos(idLivro)
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
        capitulos=controllerCapitulo.getCapitulo(livro.id)
        return render_template("menuLivro.html",capitulos=capitulos,livro=livro)
    else:
        abort(403)
        return

@app.route(
    "/livro/<int:idLivro>/capitulo/<acao>/<int:idCapitulo>",
    methods=["GET", "POST"]
)
def capitulos(acao, idLivro, idCapitulo):

    idSession = session.get("user_id")

    livro = controllerLivro.getLivroIdLivro(
        idLivro
    )
    print(f"esse é o livro.idUsuario: {livro.idUsuario}")

    if not livro:
        abort(404)

    if livro.idUsuario != idSession:
        abort(403)

    capitulo = None


    if acao == "editar":

        capitulo = controllerCapitulo.getCapitulo(
            idCapitulo
        )
        print(f"esse é o capitulo.idLivro: {capitulo.idLivro}")

        if not capitulo:
            abort(404)

        if capitulo.idLivro != idLivro:
            abort(403)

        
        if request.method == "GET":

            return render_template(
                "addCapitulo.html",
                capitulo=capitulo,
                acao="editar"
            )

        
        elif request.method == "POST":

            titulo = request.form.get(
                "titulo"
            )

            conteudo = request.form.get(
                "conteudo"
            )

            mensagem = controllerCapitulo.editarCapitulo(
                idCapitulo,
                titulo,
                conteudo
            )

            return render_template(
                "addCapitulo.html",
                capitulo=capitulo,
                mensagem=mensagem,
                acao="editar"
            )



    elif acao == "criar":

        
        if request.method == "GET":

            return render_template(
                "addCapitulo.html",
                acao="criar"
            )

        
        elif request.method == "POST":

            titulo = request.form.get(
                "titulo"
            )

            conteudo = request.form.get(
                "conteudo"
            )

            mensagem = controllerCapitulo.criarCapitulo(
                titulo,
                conteudo,
                idLivro
            )

            return render_template(
                "addCapitulo.html",
                mensagem=mensagem,
                acao="criar"
            )

    else:

        abort(404)
    



if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
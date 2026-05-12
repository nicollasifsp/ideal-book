from flask import *
from flask_sqlalchemy import *
from db import db
from model.usuarioModel import UsuarioModel
from controller.controllerUsuario import ControllerUsuario
from controller.controllerLivro import ControllerLivro


controllerUsuario=ControllerUsuario()
controllerLivro=ControllerLivro()


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///idealBook.db"
db.init_app(app)
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
@app.route("/renderBiblioteca")
def renderBiblioteca():
    return render_template("biblioteca.html")
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
        if mensagemLogin=="leitor":
            return redirect(url_for("renderBiblioteca"))
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
    conteudo=request.form["conteudo"]
    quantPag=int(request.form["quantPag"])
    imagem=request.form["imagem"]
    controllerLivro.salvarLivro(titulo,autor,descricao,conteudo,imagem,quantPag)

    

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
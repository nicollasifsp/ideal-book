from flask import *
app=Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/renderLogin")
def renderLogin():
    return render_template("login.html")

@app.route("/fazerLogin",methods=["POST"])
def fazerLogin():
    email=request.form["email"]
    senha=request.form["senha"]
    return render_template('teste1.html',email=email,senha=senha) #aqui vc manda por parametros os dados

@app.route("/renderCadastro")
def renderCadastro():
    return render_template('cadastro.html')
@app.route('/fazerCadastro',methods=["POST"])
def fazerCadastro():
    nome=request.form["nome"]
    email=request.form["email"]
    senha=request.form["senha"]
    confirmarSenha=request.form["confirmarSenha"]
    return render_template("teste.html",nome=nome,email=email,senha=senha,confirmarSenha=confirmarSenha)

if __name__=="__main__":
    app.run(debug=True)


from model.usuarioModel import UsuarioModel
from db import db
class ControllerUsuario():
    def __init__(self):
        pass

    def salvarUsuario(self,nome,email,senha,tipoUsuario): 
        usuarioExistente = UsuarioModel.query.filter_by(email=email).first()
        if not usuarioExistente:
            novoUsuario=UsuarioModel(nome=nome,email=email,senha=senha,tipoUsuario=tipoUsuario)
            db.session.add(novoUsuario)
            db.session.commit()
            return True
        else:
            return False
        
    def fazerLogin(self,email,senha):
        usuarioExistente = UsuarioModel.query.filter_by(email=email,senha=senha).first()

        if not usuarioExistente:
            return False
        else:
            tipoUsuario= db.session.query(UsuarioModel.tipoUsuario).filter_by(email=email,senha=senha).first()
            if tipoUsuario == "leitor":
                return "leitor"
            else:
                return "escritor"

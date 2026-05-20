from model.usuarioModel import UsuarioModel
from bd.db import db
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
            resultado= UsuarioModel.query.filter_by(email=email,senha=senha).first()
            return resultado    
    
    def getUserId(id):
        usuario=UsuarioModel.query.filter_by(id=id).first()
        return usuario

        

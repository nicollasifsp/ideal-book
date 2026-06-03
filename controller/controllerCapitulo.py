from model.capituloModel import CapituloModel
from database.db import db


class ControllerCapitulo():

    def __init__(self):
        pass


    def getCapitulos(self, idLivro):

        capitulos = CapituloModel.query.filter_by(
            idLivro=idLivro
        ).all()

        return capitulos


    def salvarCapitulo(self,titulo,conteudo,idLivro):
        try:
            novoCapitulo=CapituloModel(titulo=titulo,conteudo=conteudo,idLivro=idLivro)
            db.session.add(novoCapitulo)
            db.session.commit()
            return True
        except Exception as erro:
            print(f"ocorreu esse erro:\n{erro}")
            return False
    
    def getCapitulo(self,idCapitulo):
        capitulo=CapituloModel.query.filter_by(idCapitulo=idCapitulo).first()
        return capitulo
    
    def updateCapitulo(self, idCapitulo, titulo, conteudo):
        try:
            capitulo = CapituloModel.query.filter_by(idCapitulo=idCapitulo).first()

            if not capitulo:
                return False

            capitulo.titulo = titulo
            capitulo.conteudo = conteudo

            db.session.commit()
            return True

        except Exception as erro:
            print(f"ocorreu esse erro:\n{erro}")
            return False
        
    def deletarCapituloId(self,capitulo):
        try:
            db.session.delete(capitulo)
            db.session.commit()
            return True
        except Exception as erro:
            print(f"erro: {erro}")
            db.session.rollback() 
            return False
        
    def deletarCapitulos(self,idLivro):
        try:
            #aqui vc faça uma deleta em massa todos os capitulos que tem  o id livro igual o idLivro.
            CapituloModel.query.filter_by(idLivro=idLivro).delete()
            db.session.commit()
            return True
        
        except Exception as erro:
            #aqui faça um rollback
            print(f"erro:{erro}")
            db.session.rollback()
            return False
    

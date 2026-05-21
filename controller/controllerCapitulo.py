from model.capituloModel import CapituloModel
from database.db import db


class ControllerCapitulo():

    def __init__(self):
        pass


    def getCapitulo(self, idLivro):

        capitulos = CapituloModel.query.filter_by(
            idLivro=idLivro
        ).first()

        return capitulos


    def getConteudo(self, idCapitulo):

        capitulo = CapituloModel.query.filter_by(
            id=idCapitulo
        ).first()

        return capitulo


    def criarCapitulo(
        self,
        titulo,
        conteudo,
        idLivro
    ):

        try:

            novoCapitulo = CapituloModel(

                titulo=titulo,

                conteudo=conteudo,

                idLivro=idLivro

            )

            db.session.add(
                novoCapitulo
            )

            db.session.commit()

            return True

        except:

            db.session.rollback()

            return False


    def editarCapitulo(
        self,
        idCapitulo,
        titulo,
        conteudo
    ):

        try:

            capitulo = CapituloModel.query.get(
                idCapitulo
            )

            if not capitulo:
                return False

            capitulo.titulo = titulo

            capitulo.conteudo = conteudo

            db.session.commit()

            return True

        except:

            db.session.rollback()

            return False
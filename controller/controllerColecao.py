from database.db import db
from model.colecaoModel import ColecaoModel
from model.livroModel import LivroModel


class ControllerColecao:
    def __init__(self):
        pass

    def favoritarLivro(self, idUsuario, idLivro):
        try:
            existente = ColecaoModel.query.filter_by(
                idUsuario=idUsuario,
                idLivro=idLivro
            ).first()

            if existente:
                db.session.delete(existente)
                db.session.commit()
                return False

            novo = ColecaoModel(
                idUsuario=idUsuario,
                idLivro=idLivro
            )
            db.session.add(novo)
            db.session.commit()
            return True
        except Exception as erro:
            print(f"erro ao favoritar livro: {erro}")
            db.session.rollback()
            return None

    def isFavorito(self, idUsuario, idLivro):
        return (
            ColecaoModel.query.filter_by(
                idUsuario=idUsuario,
                idLivro=idLivro
            ).first()
            is not None
        )

    def getIdsColecao(self, idUsuario):
        colecao = ColecaoModel.query.filter_by(idUsuario=idUsuario).all()
        return {item.idLivro for item in colecao}

    def getLivrosColecao(self, idUsuario):
        return (
            LivroModel.query.join(
                ColecaoModel, ColecaoModel.idLivro == LivroModel.id
            )
            .filter(ColecaoModel.idUsuario == idUsuario)
            .all()
        )

    def deletarColecaoLivro(self, idLivro):
        try:
            itens = ColecaoModel.query.filter_by(idLivro=idLivro).all()
            for item in itens:
                db.session.delete(item)
            db.session.commit()
            return True
        except Exception as erro:
            print(f"erro ao deletar colecao do livro: {erro}")
            db.session.rollback()
            return False

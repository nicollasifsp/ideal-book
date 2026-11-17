from database.db import db
from sqlalchemy import UniqueConstraint


class ProgressoModel(db.Model):
    __tablename__ = "progresso"

    __table_args__ = (
        UniqueConstraint(
            "idColecao",
            "idCapitulo",
            name="uq_colecao_capitulo"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    idColecao = db.Column(
        db.Integer,
        db.ForeignKey("colecoes.id"),
        nullable=False
    )

    idCapitulo = db.Column(
        db.Integer,
        db.ForeignKey("capitulos.idCapitulo"),
        nullable=False
    )

    concluido = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    dataLeitura = db.Column(
        db.DateTime,
        nullable=True
    )

    colecao = db.relationship(
        "ColecaoModel",
        back_populates="progresso"
    )

    capitulo = db.relationship("CapituloModel")

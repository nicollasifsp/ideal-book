from database.db import db
from sqlalchemy import UniqueConstraint


class ColecaoModel(db.Model):
    __tablename__ = "colecoes"

    __table_args__ = (
        UniqueConstraint(
            "idUsuario",
            "idLivro",
            name="uq_usuario_livro"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    idUsuario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    idLivro = db.Column(
        db.Integer,
        db.ForeignKey("livros.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="quero_ler",
        nullable=False
    )

    dataAdicao = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    progresso = db.relationship(
        "ProgressoModel",
        back_populates="colecao",
        cascade="all, delete-orphan"
    )

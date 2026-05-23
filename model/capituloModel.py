from database.db import db
class CapituloModel(db.Model):

    __tablename__ = "capitulos"

    idCapitulo = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150), nullable=False)

    conteudo = db.Column(db.Text, nullable=False)

    idLivro = db.Column(
        db.Integer,
        db.ForeignKey("livros.id"),
        nullable=False
    )
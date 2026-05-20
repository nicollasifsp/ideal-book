from database.db import db

class CapituloModel(db.Model):
    __tablename__="capitulos"
    id=db.Column(db.Integer,primary_key=True)
    conteudo=db.Column(db.Text,nullable=False)
    idLivro=db.Column(
        db.Integer, 
        db.ForeignKey("livros.id"),
        nullable=False)
from bd.db import db

class UsuarioModel(db.Model):

    __tablename__="usuarios"
    
    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(60),nullable=False)
    senha=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(60),nullable=False)
    tipoUsuario=db.Column(db.String(20),nullable=False)

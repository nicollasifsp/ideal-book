from db import db

class LivroModel(db.Model):
    __tablename__="livros"
    id=db.Column(db.Integer,primary_key=True)
    titulo=db.Column(db.String,nullable=False)
    autor=db.Column(db.String,nullable=False)
    descricao=db.Column(db.String,nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    caminhaoImagem=db.Column(db.String,nullable=False,unique=True)
    quantPag=db.Column(db.Integer,nullable=False)
    

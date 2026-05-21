from model.livroModel import LivroModel
from database.db import db
class ControllerLivro():
    def __init__(self):
        pass
    def salvarLivro(self,titulo,autor,descricao,caminhoImagem,quantPag,idUsuario):
        try:
            novoLivro=LivroModel(titulo=titulo,autor=autor,descricao=descricao,caminhoImagem=caminhoImagem,quantPag=quantPag,idUsuario=idUsuario)
            db.session.add(novoLivro)
            db.session.commit()
            return True
        except Exception as erro:
            print(erro)
            return False
        
    def getLivros(self):
        livros=LivroModel.query.all()
        return livros
    
    
    def getLivrosAutor(self,idUsuario):
        livros=LivroModel.query.filter_by(idUsuario=idUsuario).all()
        return livros
    
    def getLivroIdLivro(self,idLivro):
        livro=LivroModel.query.filter_by(id=idLivro).first()
        return livro
    
    def mostrarDados(self,livros):
        for livro in livros:
            print(f"id do livro: {livro.id}\ntitulo: {livro.titulo}\n")
            print(f"")
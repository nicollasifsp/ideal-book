from model.livroModel import LivroModel
from database.db import db
class ControllerLivro():
    def __init__(self):
        pass
    def salvarLivro(self,titulo,autor,descricao,conteudo,caminhoImagem,quantPag,idUsuario):
        try:
            novoLivro=LivroModel(titulo=titulo,autor=autor,descricao=descricao,conteudo=conteudo,caminhoImagem=caminhoImagem,quantPag=quantPag,idUsuario=idUsuario)
            db.session.add(novoLivro)
            db.session.commit()
            return True
        except Exception as erro:
            print(erro)
            return False
    def getLivros(self):
        livros=LivroModel.query.all()
        return livros
    
    def getConteudo(self,id):
        livro=LivroModel.query.filter_by(id=id).first()
        return livro
    
    def getLivroAutor(idUsuario):
        livros=LivroModel.query.filter_by(idUsuario=idUsuario)
        return livros

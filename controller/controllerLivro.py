from model.livroModel import LivroModel
from db import db
class ControllerLivro():
    def __init__(self):
        pass
    def salvarLivro(self,titulo,autor,descricao,conteudo,caminhoImagem,quantPag):
        try:
            novoLivro=LivroModel(titulo=titulo,autor=autor,descricao=descricao,conteudo=conteudo,caminhoImagem=caminhoImagem,quantPag=quantPag)
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

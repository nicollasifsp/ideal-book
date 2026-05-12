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
        

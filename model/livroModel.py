class LivroModel():
    def __init__(self,titulo, descricao,autor,caminhoImagem, quantPag,conteudo):
        self__titulo=titulo
        self__descricao=descricao
        self__autor=autor
        self__caminhoImagem=caminhoImagem
        self__quantPag=quantPag
        self__conteudo=conteudo

        def getTitulo(self):
            return self__titulo
        def setTitulo(self,novoTitulo):
            self__titulo=novoTitulo
        
        def getDescricao(self):
            return self__descricao
        def setDescricao(self,novaDescricao):
            self__descricao=novaDescricao
        
        def getAutor(self):
            return self__autor
        def setAutor(self,novoAutor):
            self__autor=novoAutor

        def getQuantPag(self):
            return self__quantPag
        def setQuantPAg(self,novaQuantPag):
            self__quantPag=novaQuantPag

        def getConteudo(self):
            return self__conteudo
        def setConteudo(self,novoConteudo):
            self__conteudo=novoConteudo
        
        
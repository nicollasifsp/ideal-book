class UsuarioModel():
    def __init__(self,nome,email,senha,tipoUsuario):
        self__nome=nome
        self__email=email
        self__senha=senha
        self__tipoUsuario=tipoUsuario
    
    def getNome(self):
        return self__nome
    
    def setNome(self,novoNome):
        self__nome=novoNome

    def getEmail(self):
        return self__email
    
    def setEmail(self,novoEmail):
        self__email=novoEmail

    def getSenha(self):
        return self__senha
    def setSenha(self,novaSenha):
        self__senha=novaSenha

    def salvarRegistros(self): #caso precise passe como paramêtro o objeto
        pass

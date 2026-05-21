from model.capituloModel import CapituloModel
class ControllerCapitulo():
    def __init__(self):
        pass
    def getCapitulos(self,id):
        capitulos=CapituloModel.query.filter_by(idLivro=id).all()
        return capitulos
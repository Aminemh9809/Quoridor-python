class Pawn: # case
    def __init__(self,valeur,ligne,colonne):
       
        self.valeur = valeur
        self.ligne=ligne
        self.colonne=colonne
    
    def getValeur(self):
        return  self.valeur
        
    def setValeur(self,valeur):
        self.valeur = valeur
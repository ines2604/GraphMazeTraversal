class Pile:
    def __init__(self):
        self.elements=[]
    def pile_vide(self):
        return(len(self.elements)==0)
    def empiler(self,x):
        self.elements.append(x)
    def depiler(self):
        assert(self.pile_vide()==False)
        return self.elements.pop()
    def taille_pile(self):
        return len(self.elements)
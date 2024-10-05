class File:
    def __init__(self):
        self.elements=[]
    def file_vide(self):
        return(len(self.elements)==0)
    def enfiler(self,x):
        self.elements.append(x)
    def defiler(self):
        return self.elements.pop(0)
    def taille_file(self):
        return(len(self.elements))
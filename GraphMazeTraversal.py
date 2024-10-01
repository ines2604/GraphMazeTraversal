from pile import Pile
from file import File

import pygame
from pygame.locals import *

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Taille de la fenêtre
WINDOW_SIZE = (500, 500)

def draw_maze(screen, graphe, explores, path):
    cell_size = min(WINDOW_SIZE) // max(graphe.largeur, graphe.hauteur)
    
    # Dessiner les cellules visitées
    for i in range(graphe.hauteur):
        for j in range(graphe.largeur):
            node = (i, j)
            x = j * cell_size
            y = i * cell_size
            if node in explores:
                pygame.draw.rect(screen, (173, 216, 230), (x, y, cell_size, cell_size))  # Bleu clair pour les cellules visitées
            if node in path:
                pygame.draw.rect(screen, (255, 223, 186), (x, y, cell_size, cell_size))  # Couleur orange pour le chemin

    # Dessiner les murs
    for i in range(graphe.hauteur):
        for j in range(graphe.largeur):
            node = (i, j)
            x = j * cell_size
            y = i * cell_size
            if node in graphe.graph:
                adjacents = graphe.adjacence_noeud(node)
                for adj in adjacents:
                    adj_x, adj_y = adj
                    if not graphe.graph[node][adj]:
                        if adj_x > i:  # Mur vers le bas
                            pygame.draw.line(screen, BLACK, (x, y + cell_size), (x + cell_size, y + cell_size), 3)
                        elif adj_x < i:  # Mur vers le haut
                            pygame.draw.line(screen, BLACK, (x, y), (x + cell_size, y), 3)
                        elif adj_y > j:  # Mur vers la droite
                            pygame.draw.line(screen, BLACK, (x + cell_size, y), (x + cell_size, y + cell_size), 3)
                        elif adj_y < j:  # Mur vers la gauche
                            pygame.draw.line(screen, BLACK, (x, y), (x, y + cell_size), 3)
            else:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size))

    # Dessiner le cadre extérieur
    pygame.draw.rect(screen, BLACK, (0, 0, graphe.largeur * cell_size, graphe.hauteur * cell_size), 3)

                
class Graphe:
    def __init__(self,largeur,hauteur):
        self.graph = {}
        self.hauteur=hauteur
        self.largeur=largeur

    def ajouter_noeud(self, coordonnees):
        if coordonnees not in self.graph:
            self.graph[coordonnees] = {}

    def ajouter_arc(self, coordonnees1, coordonnees2, porte=False):
        if coordonnees1 in self.graph and coordonnees2 in self.graph:
            self.graph[coordonnees1][coordonnees2] = porte
            self.graph[coordonnees2][coordonnees1] = porte

    def lister_noeuds(self):
        return list(self.graph.keys())

    def lister_arcs(self):
        arcs = []
        for sommet in self.graph:
            for voisin in self.graph[sommet]:
                if (sommet, voisin) not in arcs and (voisin, sommet) not in arcs:
                    arcs.append((sommet, voisin))
        return arcs

    def adjacence_noeud(self, coordonnees):
        if coordonnees in self.graph:
            return list(self.graph[coordonnees].keys())

    def afficher_graphe(self):
        for sommet in self.graph:
            print(f"Sommet {sommet}:")
            for voisin in self.graph[sommet]:
                if self.graph[sommet][voisin]:
                    porte = "avec porte"
                else:
                    porte = "sans porte"
                print(f"  - Voisin {voisin} {porte}")

    def successeur_avec_cle(self, etat):
        i, j = etat
        l = self.graph[(i, j)]
        return l

    def successeur_sans_cle(self, etat):
        succ = []
        for voisin, porte in self.graph[etat].items():
            succ.append((voisin[0], voisin[1]))
        return succ

    def verifetat(self, etat, explores, accessibles):
        if etat in explores or etat in accessibles:
            return True
        else:
            return False

    def successeurs(self, etat, explores, accessibles):
        succ = []
        if etat in self.graph:
            for voisin, porte in self.graph[etat].items():
                if not porte:  # Vérifier si le mur est ouvert (porte=True)
                    continue
                if self.verifetat(voisin, explores, accessibles):
                    continue
                succ.append(voisin)
        return succ

    def dfs(self, etat_initial, etat_final, accessibles, explores):
        p = Pile()
        p.empiler((etat_initial, [etat_initial]))
        while not p.pile_vide():
            x, path = p.depiler()
            explores.append(x)
            if x == etat_final:
                return path
            for s in reversed(self.successeurs(x, explores, accessibles)):
                if not s in explores:
                    accessibles.append(s)
                    path_with_s = path + [s]
                    p.empiler((s, path_with_s))
                
    
    def bfs(self, etat_initial, etat_final, accessibles, explores):
        f = File()
        f.enfiler((etat_initial, [etat_initial]))
        while not f.file_vide():
            x, path = f.defiler()
            explores.append(x)
            if x == etat_final:
                return path
            for s in self.successeurs(x, explores, accessibles):
                if not s in explores:
                    accessibles.append(s)
                    f.enfiler((s, path + [s]))
    
    def ldfs(self,l,etat_initial,etat_final,accessibles,explores):
        p = Pile()
        p.empiler((etat_initial, [etat_initial]))
        limite=0
        while not (p.pile_vide()) and limite<=l:
            x, path = p.depiler()
            explores.append(x)
            for s in reversed(self.successeurs(x, explores, accessibles)):
                if s == etat_final:
                    return path+[s]
                if not s in explores:
                    accessibles.append(s)
                    path_with_s = path + [s]
                    p.empiler((s, path_with_s))
            limite+=1
    
    def ldfs_iteratif(self, etat_initial, etat_final):
        l = 0
        while True:
            accessibles=[]
            explores=[]
            res = self.ldfs(l, etat_initial, etat_final, accessibles, explores)
            if res is not None:
                return res
            l += 1


class Personne:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_person(screen, cell_size, personne):
    x = personne.x * cell_size
    y = personne.y * cell_size
    pygame.draw.circle(screen, (255, 0, 0), (x + cell_size // 2, y + cell_size // 2), cell_size // 4)  # Personne en rouge


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Maze Solver")

    clock = pygame.time.Clock()
    running = True

    g = Graphe(3,3)
    g.ajouter_noeud((0, 0))
    g.ajouter_noeud((0, 1))
    g.ajouter_noeud((0, 2))
    g.ajouter_noeud((1, 0))
    g.ajouter_noeud((1, 1))
    g.ajouter_noeud((1, 2))
    g.ajouter_noeud((2, 0))
    g.ajouter_noeud((2, 1))
    g.ajouter_noeud((2, 2))

    g.ajouter_arc((0, 0), (0, 1), porte=True)
    g.ajouter_arc((0, 0), (1, 0), porte=True)
    g.ajouter_arc((0, 1), (1, 1), porte=True)
    g.ajouter_arc((0, 1), (0, 2), porte=True)
    g.ajouter_arc((0, 2), (1, 2), porte=False)
    g.ajouter_arc((1, 0), (1, 1), porte=False)
    g.ajouter_arc((1, 0), (2, 0), porte=True)
    g.ajouter_arc((1, 1), (1, 2), porte=True)
    g.ajouter_arc((1, 1), (2, 1), porte=False)
    g.ajouter_arc((1, 2), (2, 2), porte=True)
    g.ajouter_arc((2, 0), (2, 1), porte=False)
    g.ajouter_arc((2, 1), (2, 2), porte=False)

    cell_size = min(WINDOW_SIZE) // max(g.largeur, g.hauteur)
    personne = Personne(0, 0)  # Personne commençant à la position (0, 0)

    # Trouver le chemin avec l'algorithme de votre choix
    explores = []
    chemin = g.dfs((0, 0), (2, 2), [], explores)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(WHITE)
        draw_maze(screen, g, explores, chemin)  # Afficher le labyrinthe avec les cellules visitées et le chemin
        draw_person(screen, cell_size, personne)  # Dessiner la personne

        # Si le chemin n'est pas vide, déplacer la personne vers la prochaine étape du chemin
        if chemin:
            next_step = chemin.pop(0)
            personne.y, personne.x = next_step
            pygame.display.flip()
            pygame.time.wait(500)  # Attendre 500 millisecondes entre chaque déplacement

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
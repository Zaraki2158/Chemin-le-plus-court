import random
import matplotlib.pyplot as plt


class Cellule:
    #constructeur principal de la classe Cellule
    def __init__(self, colonnes, pos):
        # Génération aléatoire des murs de la cellule en tant qu'attribut de la classe Cellule
        self.bas = random.randint(1, 5)
        self.droit = random.randint(1, 5)
        #on vérifie si le mur est sur la première ligne
        if pos <= colonnes:
            self.haut = random.randint(1, 5)    #si oui on créer un mur aléatoire    
        else:
            self.haut = 0   #sinon on met 0 et on récuperera le mur de la cellule d'avant
        #on vérifie si le mur est sur la premiere colonne
        if pos % colonnes == 0:
            self.gauche = random.randint(1, 5)  #si oui on créer un mur aléatoire  
        else:
            self.gauche = 0      #sinon on met 0 et on récuperera le mur de la cellule d'au dessus


class Grille:
    #constructeur princiapl de la classe Grille
    def __init__(self, lignes, colonnes):
        #on initialise les attributs
        self.lignes = lignes
        self.colonnes = colonnes
        self.pos = lignes*colonnes
        self.cellulesT = [Cellule(self.colonnes, i) for i in range(self.pos)]
        self.cellules = {i: float('inf') for i in range(self.pos)}
        
        #tableau contenant cellule vosin et épaisseur
        cells = []
        
        #on créer le dictionnaire
        for i in range(self.pos):
            cell = self.cellulesT[i]    #on prend la cellule à la position i
            
            #on regarde si la cellule n'est pas une cellule se situant sur la premiere ligne
            if not i <= colonnes:   
                if cell.haut == 0:  #on regarde si on a pas de mur 
                    cells.append([i-colonnes, self.cellulesT[i-colonnes].bas])  #si oui on prend l'attribut bas de la cellule d'au dessus
                else:
                    cells.append([i-colonnes, cell.haut])   #sinon on prend l'attribut haut de notre cellule à la position i
            #on regarde si la cellule n'est pas une cellule se situant sur la premiere colonne
            if not i % colonnes == 0:
                if cell.gauche == 0:    #on regarde si on a pas de mur 
                    cells.append([i-1, self.cellulesT[i-1].droit])   #si oui on prend l'attribut bas de la cellule d'au dessus
                else:
                    cells.append([i-1, cell.gauche])    #sinon on prend l'attribut gauche de la cellule i
            #on regarde si la cellule n'est pas une cellule se situant sur la dernière colonne
            if not (i+1) % colonnes == 0:
                cells.append([i+1, cell.droit])
            #on regarde si la cellule n'est pas une cellule se situant sur la dernière ligne
            if not i > (lignes*colonnes)-colonnes:
                cells.append([i+colonnes, cell.bas])
            
            #on rajoute dans notre dictionnaire à la position i le tableau cells
            self.cellules[i] = cells
            cells = []  #on reinitialise notre tableau
    
    #fonction pour afficher la cellule et l'épaisseur de chacun de ces mots
    def afficher_murs(self):
        for i in range(self.pos):
            cellG, cellH = self.cellulesT[i].gauche, self.cellulesT[i].haut
            if cellG == 0:
                cellG = self.cellulesT[i-1].droit
            if cellH == 0:
                cellH = self.cellulesT[i-self.colonnes].bas
            print(
                f"Cellule", i, f": haut = {cellH}, droite = {self.cellulesT[i].droit}, bas = {self.cellulesT[i].bas}, gauche = {cellG}")

    #fonction pour afficher la grille et la grille percé avec le chemin
    def afficher_grille(self, chemin):
        # Initialise la figure et le système de coordonnées
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.colonnes+2)
        ax.set_ylim(0, (self.lignes+2)*2)
        ax.invert_yaxis()
        ax.set_axis_off()
        
        #fonction pour afficher une grille
        def afficher_cellule(x, y):
            for i in range(self.pos):
                cellule = self.cellulesT[i]
                # Mur en haut
                if cellule.haut > 0:
                    ax.plot([x, x + 1], [y, y],
                            linewidth=cellule.haut*2, color='#006666')
                # Mur à droite
                if cellule.droit > 0:
                    ax.plot([x + 1, x + 1], [y, y + 1],
                            linewidth=cellule.droit*2, color='#006666')
                # Mur en bas
                if cellule.bas > 0:
                    ax.plot([x, x + 1], [y+1, y+1],
                            linewidth=cellule.bas*2, color='#006666')
                # Mur à gauche
                if cellule.gauche > 0:
                    ax.plot([x, x], [y, y + 1],
                            linewidth=cellule.gauche*2, color='#006666')
                if x == self.colonnes:
                    x, y = 1, y+1
                else:
                    x = x+1
                    
        # Affiche les deux grilles
        afficher_cellule(1, 1)
        afficher_cellule(1, 2+self.lignes)
        
        #Fonction pour afficher le chemin 
        def afficher_chemin(x1, y1, liste, coul, epaisseur, colonnes):
            x2, y2 = x1, y1
            for j in range(len(liste)-1):
                if liste[j+1] == liste[j]-1:
                    x2 = x2-1
                elif liste[j+1] == liste[j]+1:
                    x2 = x2+1
                elif liste[j+1] == liste[j]-colonnes:
                    y2 = y2-1
                elif liste[j+1] == liste[j]+colonnes:
                    y2 = y2+1
                ax.plot([x1, x2], [y1, y2], linewidth=epaisseur, color=coul)
                x1, y1 = x2, y2
        #Pour afficher les murs percé on a fait un chemin blanc
        afficher_chemin(1.5, 2.5+self.lignes, chemin,'white', 6, self.colonnes)
        #chemin en rouge
        afficher_chemin(1.5, 2.5+self.lignes, chemin, 'red', 2, self.colonnes)

        plt.show()

    #Récupere le cout et la liste du chemin
    def chemin_cout(self, s):
        #Fonction poyr récuperer le minimum donnée en CM
        def minimum(dico):
            m = float('inf')
            for k in dico:  # parcours des clés
                if dico[k] < m:
                    m = dico[k]
                    i = k
            return i
        #fonction pour récuperer la liste des prédecesseur et le cout, donné en CM
        def dijkstra_pred(G, s):
            D = {}  # tableau final des distances minimales
            d = {k: float('inf') for k in G}  # distances initiales infinies
            d[s] = 0  # sommet de départ
            P = {}  # liste des prédécesseurs
            long = len(G)-1
            while len(d) > 0:  # fin quand d est vide
                # sommet de distance minimale pour démarrer une étape
                k = minimum(d)
                for i in range(len(G[k])):  # on parcourt les voisins de k
                    v, c = G[k][i]  # v voisin de k, c la distance à k
                    if v not in D and v <= long and v >= 0:  # si v n'a pas été déjà traité
                        if d[v] > d[k]+c:  # est-ce plus court en passant par k ?
                            d[v] = d[k]+c
                            P[v] = k  # stockage du prédécesseur de v
                D[k] = d[k]  # copie du sommet et de la distance dans D
                del(d[k])  # suppression du sommet de d
            # on retourne aussi la liste des prédécesseurs
            return chemin(P, long)+[long], D[long]
        #FOnction pour avoir le chemin grâce à la liste des prédecesseur
        def chemin(dico, s):
            if s == 0:
                return[]
            else:
                k = dico[s]
                return chemin(dico, k)+[k]
        G = self.cellules    #Attribut pour lancement de la fonction djikstra_pred()
        return dijkstra_pred(G, s)  #Renvoie le résultat de l'appel de la fonction djikstra_pred(G,s)

#Fonction main
def main(lignes, colonnes):
    #création de la grille
    ma_grille = Grille(lignes, colonnes)
    #récuperer chemin et cout
    chemin, cout = ma_grille.chemin_cout(0)
    #inverser chemin pour avoir du départ jusqu'a l'arrivée
    #on affiche les deux grilles avec le chemin grâce à l'appel de la fonction afficher_grille()
    ma_grille.afficher_grille(chemin)
    #affichage du message dans la console
    mes = "Chemin : "
    for i in chemin:
        mes = mes+str(i)
        if chemin.index(i)<len(chemin)-1:
            mes= mes+", "
    mes = mes+"\nCoût : "+str(cout)
    print(mes)

#Fonction main avec toutes les information cachés à l'utilisateur
def mainProgrammeur(lignes, colonnes):
    #création de la grille
    ma_grille = Grille(lignes, colonnes)
    #récuperer chemin et cout
    chemin, cout = ma_grille.chemin_cout(0)
    #inverser chemin pour avoir du départ jusqu'a l'arrivée
    chemin.reverse()
    #on affiche les deux grilles avec le chemin grâce à l'appel de la fonction afficher_grille()
    ma_grille.afficher_grille(chemin)
    #affichage du message dans la console
    mes = "Chemin : "
    for i in chemin:
        mes = mes+str(i)
        if chemin.index(i)<len(chemin)-1:
            mes= mes+", "
    mes = mes+"\nCoût : "+str(cout)
    mes = mes+"\n\n"+str(ma_grille.cellules)
    mes = mes+"\n"
    print(mes)
    print(ma_grille.afficher_murs())


main(3,4)


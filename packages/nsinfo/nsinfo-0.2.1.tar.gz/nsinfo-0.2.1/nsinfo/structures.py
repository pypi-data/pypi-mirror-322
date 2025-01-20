class Pile:
    def __init__(self):
        self.elements = []

    def est_vide(self):
        return len(self.elements) == 0

    def empiler(self, element):
        self.elements.append(element)

    def depiler(self):
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.elements.pop()

    def sommet(self):
        if self.est_vide():
            raise IndexError("La pile est vide")
        return self.elements[-1]


class File:
    def __init__(self):
        self.elements = []

    def est_vide(self):
        return len(self.elements) == 0

    def enfiler(self, element):
        self.elements.append(element)

    def defiler(self):
        if self.est_vide():
            raise IndexError("La file est vide")
        return self.elements.pop(0)


class Graphe:
    def __init__(self):
        self.adjacence = {}

    def ajouter_sommet(self, sommet):
        if sommet not in self.adjacence:
            self.adjacence[sommet] = []

    def ajouter_arete(self, sommet1, sommet2):
        if sommet1 not in self.adjacence:
            self.ajouter_sommet(sommet1)
        if sommet2 not in self.adjacence:
            self.ajouter_sommet(sommet2)
        self.adjacence[sommet1].append(sommet2)
        self.adjacence[sommet2].append(sommet1)

    def voisins(self, sommet):
        return self.adjacence.get(sommet, [])


def sous_tableau(tableau, debut, fin):
    resultat = []
    for i in range(debut, fin):
        resultat.append(tableau[i])
    return resultat


def tri_insertion(tableau):
    for i in range(1, len(tableau)):
        element = tableau[i]
        j = i
        while j > 0 and tableau[j - 1] > element:
            tableau[j] = tableau[j - 1]
            j -= 1
        tableau[j] = element
    return tableau


def recherche_dichotomique(tableau, valeur):
    debut = 0
    fin = len(tableau) - 1
    while debut <= fin:
        milieu = (debut + fin) // 2
        if tableau[milieu] == valeur:
            return milieu
        elif tableau[milieu] < valeur:
            debut = milieu + 1
        else:
            fin = milieu - 1
    return -1


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def factorielle(n):
    if n == 0:
        return 1
    return n * factorielle(n - 1)


def parcours_profondeur(graphe, sommet, visites=None):
    if visites is None:
        visites = set()
    visites.add(sommet)
    for voisin in graphe.voisins(sommet):
        if voisin not in visites:
            parcours_profondeur(graphe, voisin, visites)
    return visites


def parcours_largeur(graphe, sommet):
    visites = set()
    file = File()
    file.enfiler(sommet)
    while not file.est_vide():
        actuel = file.defiler()
        if actuel not in visites:
            visites.add(actuel)
            for voisin in graphe.voisins(actuel):
                file.enfiler(voisin)
    return visites

class Noeud:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant


class ListeChainee:
    def __init__(self):
        self.tete = None

    def est_vide(self):
        return self.tete is None

    def ajouter(self, valeur):
        nouveau_noeud = Noeud(valeur, self.tete)
        self.tete = nouveau_noeud

    def car(self):
        if self.est_vide():
            raise ValueError("Liste vide")
        return self.tete.valeur

    def cdn(self):
        if self.est_vide():
            raise ValueError("Liste vide")
        reste = ListeChainee()
        reste.tete = self.tete.suivant
        return reste

    def afficher(self):
        elements = []
        courant = self.tete
        while courant:
            elements.append(courant.valeur)
            courant = courant.suivant
        return elements

def f():
    f()
f()
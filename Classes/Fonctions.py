import random
import numpy as np
import csv

def exponentiation_rapide(a: int, e: int, p: int) -> int:
    """Calcul a^e mod p avec l'exponentiation rapide
    """
    a_pow: int = a
    resultat: int
    j = 0
    p_bin = str("".join(reversed(format(e, 'b')))) # Converti e en binaire et l'inverse
    if (p_bin[0] == '1'):
        resultat = a
    else:
        resultat = 1
    for i in p_bin[1:]:  # converti le nombre e en binaire et l'inverse
        j += 1
        a_pow = a_pow * a_pow % p
        # print(a, "puissance", j, "=", a_pow)
        if i == '1':
            resultat = (resultat * a_pow) % p
            # print("resultat =", resultat)
    return resultat

def rabbin_miller(p: int, a: int) -> bool:
    """Effectue le test de Rabbin Miller sur un nombre n
    vérification si p est pair ou égal à 1
    Calcul de s et d tel que p = (2^s)*d+1
    On calcul a^d mod p. On vérifie si a^d = 1 mod p
    On calcul les a^(2^r) mod p successifs. Pour chacun d'entre eux, on vérifie que a^(2^r)*a^d = -1
    Retourne True si le test fonctionne
    Retourne False si le test échoue
    """

    if (p % 2 == 0) | (p == 1) :
        return False
    d: int
    s: int = 1
    diviseur: int = 2

    # Calcul de s et d tel que p = (2^s)*d+1
    while (p - 1) % (diviseur * 2) == 0:
        s += 1
        diviseur = diviseur * 2
    d = (p - 1) // (diviseur)
    # print("s =", s, "d =", d)

    a_d = exponentiation_rapide(a, d, p)  # calcule a^d mod p
    # print("a^d =", a_d, "d =", d, "mod", p)
    if (a_d == 1): # si a^d = 1 mod p
        return True
    a_pow: int = a_d
    if (s - 1) == 0: # range(0,0) donne un tableau vide, on doit l'initialiser manuellement dans ce cas
        liste_r = [0]
    else:
        liste_r = range(s - 1)

    for r in liste_r:
        # print("a^(2^r*d) =", a_pow, "r =", r)
        if a_pow == p - 1:
            return True
        a_pow = (a_pow * a_pow) % p
    return False

def rabbin_miller_boucle(nb_premier:int) -> bool:
    est_premier: bool = True
    i=0
    while (i != 10) & (est_premier):  # Fais un test de Rabbin Miller sur 10 itérations
        i += 1
        a: int = random.randint(0, nb_premier)
        while (a % nb_premier) == 0:
            a: int = random.randint(0, nb_premier)

        est_premier = rabbin_miller(nb_premier, a)
        # print("test Rabin Miller pour p =", nb_premier, "et a =", a, "est", est_premier)
    return est_premier

def gen_nbr_premier(max: int) -> int:
    """génère un nombre premier plus petit que max"""
    nb_premier: int
    est_premier: bool = False
    i: int
    while (est_premier == False):
        i = 0
        nb_premier = random.randint(3, max)
        # print("-------------------------")
        est_premier = rabbin_miller_boucle(nb_premier)
    return nb_premier



def gen_nbr_premier_produit_V2(bit_max:int):
    '''Génère un nombre premier p tel que p-1 soit le produit de n nombres premier

    bit_max : le nombre de bit sur lequel est écris le nombre premier.
    On soustrait 1 car on multiplie le nombre p-1 par 2 (pour s'assurer qu'il est pair)

    '''

    bit_max = bit_max - 1
    max = pow(2,bit_max)

    est_premier = False
    while not est_premier:
        p = 2
        p_facteur = gen_nbr_premier(max)
        p = p * p_facteur + 1
        print("------------")
        print(p)
        est_premier = rabbin_miller_boucle(p)
    print("---Nombre premier final---")
    print(p)
    print(p_facteur)
    return p, p_facteur

def generateur_facteur_V2(p:int, p_facteur:int):
    '''Calul l'élément générateur à partir du théorème de Lagrange'''
    est_generateur = False
    while not est_generateur:
        est_generateur = True
        g: int = random.randint(1, p - 1)
        print("--------------------")
        print(g)
        print("--Facteurs--")
        resultat1 = exponentiation_rapide(g, 2, p)
        resultat2 = exponentiation_rapide(g, p_facteur, p)
        resultat3 = exponentiation_rapide(g, p-1, p)
        print("avec 2 :", resultat1, "avec l'autre:", resultat2, "et ça fait :", resultat3)
        if (resultat1 == 1) | (resultat2 == 1):
            est_generateur = False
            print("c'est pas bon")

    print("element generateur")
    print(g)
    return g



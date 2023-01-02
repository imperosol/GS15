import random
import numpy as np
import csv


def bourrage_zero(nbr_bin: str, taille: int) -> str:
    return nbr_bin.zfill(taille)


def exponentiation_rapide(a: int, e: int, p: int) -> int:
    """
    Calcul a^e mod p avec l'exponentiation rapide
    """
    a_pow: int = a
    resultat: int
    j = 0
    p_bin = str("".join(reversed(format(e, 'b'))))  # Converti e en binaire et l'inverse
    if (p_bin[0] == '1'):
        resultat = a
    else:
        resultat = 1
    for i in p_bin[1:]:  # converti le nombre e en binaire et l'inverse
        j += 1
        a_pow = a_pow * a_pow % p
        if i == '1':
            resultat = (resultat * a_pow) % p
    return resultat


def rabbin_miller(p: int, a: int) -> bool:
    """
    Effectue le test de Rabbin Miller sur un nombre n
    vérification si p est pair ou égal à 1
    Calcul de s et d tel que p = (2^s)*d+1
    On calcul a^d mod p. On vérifie si a^d = 1 mod p
    On calcul les a^(2^r) mod p successifs. Pour chacun d'entre eux, on vérifie que a^(2^r)*a^d = -1
    Retourne True si le test fonctionne
    Retourne False si le test échoue
    """

    if (p % 2 == 0) | (p == 1):
        return False
    d: int
    s: int = 1
    diviseur: int = 2

    # Calcul de s et d tel que p = (2^s)*d+1
    while (p - 1) % (diviseur * 2) == 0:
        s += 1
        diviseur = diviseur * 2
    d = (p - 1) // (diviseur)

    a_d = exponentiation_rapide(a, d, p)  # calcule a^d mod p
    if (a_d == 1):  # si a^d = 1 mod p
        return True
    a_pow: int = a_d
    if (s - 1) == 0:  # range(0,0) donne un tableau vide, on doit l'initialiser manuellement dans ce cas
        liste_r = [0]
    else:
        liste_r = range(s - 1)

    for r in liste_r:
        if a_pow == p - 1:
            return True
        a_pow = (a_pow * a_pow) % p
    return False


def rabbin_miller_boucle(nb_premier: int) -> bool:
    est_premier: bool = True
    i = 0
    while (i != 100) & (est_premier):  # Fais un test de Rabbin Miller sur 100 itérations
        i += 1
        a: int = random.randint(0, nb_premier)
        while (a % nb_premier) == 0:
            a: int = random.randint(0, nb_premier)

        est_premier = rabbin_miller(nb_premier, a)
        # print("test Rabin Miller pour p =", nb_premier, "et a =", a, "est", est_premier)
    return est_premier


def gen_nbr_premier(max: int) -> int:
    """
    génère un nombre premier plus petit que max
    """

    nb_premier: int
    est_premier: bool = False
    i: int
    while (est_premier == False):
        i = 0
        nb_premier = random.randint(3, max)
        est_premier = rabbin_miller_boucle(nb_premier)
    return nb_premier


def gen_nbr_premier_produit(bit_max: int) -> (int, int):
    """
    Génère un nombre premier p tel que p-1 soit le produit de n nombres premier

    bit_max : le nombre de bit sur lequel est écris le nombre premier.
    On soustrait 1 car on multiplie le nombre p-1 par 2 (pour s'assurer qu'il est pair)

    """

    bit_max = bit_max - 1
    max = pow(2, bit_max)

    est_premier = False
    while not est_premier:
        p = 2
        p_facteur = gen_nbr_premier(max)
        p = p * p_facteur + 1
        est_premier = rabbin_miller_boucle(p)
    return p, p_facteur


def generateur_facteur(p: int, p_facteur: int):
    """
    Calcul l'élément générateur à partir du théorème de Lagrange
    """
    est_generateur = False
    while not est_generateur:
        est_generateur = True
        g: int = random.randint(1, p - 1)
        resultat1 = exponentiation_rapide(g, 2, p)
        resultat2 = exponentiation_rapide(g, p_facteur, p)
        resultat3 = exponentiation_rapide(g, p - 1, p)
        if (resultat1 == 1) | (resultat2 == 1):
            est_generateur = False
    return g

def pgcd(a: int, b: int):
    """
    Calcul du PGCD avec l'algorithme d'Euclide
    """
    r0: int
    r1: int
    temp: int
    if a >= b:
        r0 = a
        r1 = b
    else:
        r0 = b
        r1 = a

    r = 1
    while r1 > 0:
        temp = r0 % r1
        r0 = r1
        r1 = temp
    return r0


def bezout(a: int, b: int):
    """
    Calcul de l'identité de Bezout avec l'algorithme d'Euclide étendu
    """
    q: int
    x0: int = 1
    x1: int = 0
    y0: int = 0
    y1: int = 1
    temp: int
    r0: int
    r1: int
    i: int = 0
    if a >= b:
        r0 = a
        r1 = b
    else:
        r0 = b
        r1 = a
    while r1 > 0:
        i += 1

        q = r0 // r1
        temp = r0 - q * r1
        r0 = r1
        r1 = temp

        temp = q * x1 + x0
        x0 = x1
        x1 = temp

        temp = q * y1 + y0
        y0 = y1
        y1 = temp
    if i % 2 == 0:
        y0 = -1 * y0
    else:
        x0 = -1 * x0
    if a >= b:
        return x0, y0
    else:
        return y0, x0


def inverse(a: int, m: int):
    x, y = bezout(a, m)
    return x

import random


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
        #print(a, "puissance", j, "=", a_pow)
        if i == '1':
            resultat = (resultat * a_pow) % p
            #print("resultat =", resultat)
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



def gen_nbr_premier(max: int) -> int:
    """génère un nombre premier plus petit que max"""
    nb_premier: int
    est_premier: bool = False
    i: int
    while (est_premier == False):
        i = 0
        nb_premier = random.randint(3,max)
        print("-------------------------")
        est_premier = True
        while (i != 10) & (est_premier): #Fais un test de Rabbin Miller sur 10 itérations
            i += 1
            a: int = random.randint(0, max)
            while ( a % nb_premier ) == 0 :
                a: int = random.randint(0, max)

            est_premier = rabbin_miller(nb_premier, a)
            print("test Rabin Miller pour p =", nb_premier, "et a =", a, "est", est_premier)

    return nb_premier

def gen_pg() -> (int, int):
    """génère un nombre premier p et un nombre générateur g de l'ensemble Zp"""
    p: int
    g: int

    return p, g


# Retourne une clée publique et clé privée
def init_cle(g: int, p: int) -> (int, int):
    cle_publique: int
    cle_privee: int

    return cle_publique, cle_privee


# Calcul de g générateur de Zp
def generateur(p:int) -> int:
    """Création d'un élément générateur g d'un ensemble Zp

    TODO
    """
    g: int
    return g

def gen_cle_commune_alice() -> (int, int, int):
    """Calcul de p, g et a de Alice avec le protocole de Diffie Hellman"""
    max: int = pow(2, 2048)
    p: int = gen_nbr_premier(max) # génération d'un nombre premier de 2048 bits
    g: int = generateur(p) # Calcul de l'élément générateur de Zp
    a: int = exponentiation_rapide(g, random.randint(1, p-1), p) # Calcul de A = g^a mop p
    return p, g, a

def gen_cle_commune_bob(p: int, g:int, a:int) -> (int, int):
    """Calcul de B à partir de p, g et A"""
    b: int = exponentiation_rapide(g, random.randint(1, p-1), p)
    k_bob: int = a * b
    return b, k_bob

def main():
    p, g, a = gen_cle_commune_alice()
    b, k_bob = gen_cle_commune_bob(p, g, a)
    k_alice = b*a


# Calcul de g^a mod p

# print(exponentiation_rapide(5, 7, 15))
gen_nbr_premier(pow(2,2048))
# print(rabbin_miller(23,10))
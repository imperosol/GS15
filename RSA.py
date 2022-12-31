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


def calcul_cle_secrete(e: int, phi: int) -> int:
    d: int = 2
    test: int
    inverse: bool = False
    while (inverse == False) & (d < phi): #test pour chaque d entre 3 et phi s'il est l'inverse de e
        d = d + 1
        print(d)
        test = e*d
        while (test > phi):
            test = test % phi
            if (test == 1): #Si e*d = 1 mod phi
                inverse = True
    return d


def parametre_rsa() -> (int, int, int):
    """ Calcul des clés pour rsa
    On génère d'abord p et q premiers qui permettent de déterminer la premier clé n
    Puis on calcul phi et e premier à phi
    n et e sont les clés publiques
    On calcule alors d inverse de e mod phi
    d est la clé secrète"""
    max: int = pow(2, 12)
    p: int = gen_nbr_premier(max)
    q: int = gen_nbr_premier(max)
    n = p*q
    phi = (p-1)*(q-1)
    e: int = gen_nbr_premier(phi)
    d = calcul_cle_secrete(e, phi) ############Fonction longue si max supérieur à 12 bits
    print("-------------------------")
    print("max=", max)
    print("-------------------------")
    print("p=", p) 
    print("-------------------------")
    print("q=", q) 
    print("-------------------------")
    print("n=", n)
    print("-------------------------")
    print("phi=", phi)
    print("-------------------------")
    print("e=", e)
    print("-------------------------")
    print("d=", d)
    return n, e, d

'''
n, e, d = parametre_rsa ()
m: int = random.randint(3,4096)   #modifier pour l'adapter au projet
print("m avant signature : ", m)
sigM: int = exponentiation_rapide(m, d, n) #signature d'une clé/message
verifM: int = exponentiation_rapide(sigM, e, n) #verification de la signature
print("Verification signature : ", verifM)
stop = input('Entrer pour terminer')

'''
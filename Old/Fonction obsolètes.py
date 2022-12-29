def generateur_facteur(p:int, p_facteur):
    '''Calul l'élément générateur à partir du théorème de Lagrange'''
    est_generateur = False
    while not est_generateur:
        est_generateur = True
        g: int = random.randint(1, p - 1)
        print("--------------------")
        print(g)
        print("--Facteurs--")
        for facteur in p_facteur:
            resultat = exponentiation_rapide(g, facteur, p)
            print(resultat)
            if resultat == 1:
                est_generateur = False
                break
    print("element generateur")
    print(g)
    return g

# Calcul de g générateur de Zp
def generateur(p:int) -> int:
    '''Anicen algo obsolète'''

    est_valide: bool = False
    while not est_valide:
        est_valide = True
        g: int = random.randint(1, p-1)
        nb: int = g
        i = 1
        print("----------")
        print(g)
        while est_valide & (i < (p-1) // 2):
            nb = nb * g % p
            i += 1
            # print(nb)
            if (nb == 1):
                est_valide = False
    return g

def param_pg() -> (int, int):
    """Calcul de p et g pour le protocole de Diffie Hellman"""
    max: int = pow(2, 2048)
    p: int = gen_nbr_premier(max) # génération d'un nombre premier de 2048 bits
    g: int = generateur(p) # Calcul de l'élément générateur de Zp
    return p, g

def gen_nbr_premier_produit(bit_max:int, n:int):
    '''Génère un nombre premier p tel que p-1 soit le produit de n nombres premier

    bit_max : le nombre de bit sur lequel est écris le nombre premier.
    On soustrait 1 car on multiplie le nombre p-1 par 2 (pour s'assurer qu'il est pair)

    '''

    bit_max = bit_max - 1
    bit_n = bit_max // n # bit qu'ont les facteur du nombre p-1
    max_n = pow(2, bit_n)
    bit_reste = bit_max % n # bit qu'à le dernier facteur du nombre p-1
    max_reste = pow(2, bit_reste)

    est_premier = False
    while not est_premier:
        p_facteur = [2]
        p = 2
        for i in range(n):
            p_facteur.append(gen_nbr_premier(max_n))
            p = p * p_facteur[i+1]

        if bit_reste == 1:
            p = p * 2
            p_facteur[0] = 4
        if bit_reste != 0:
            p_facteur.append(gen_nbr_premier(max_reste))
            p = p * p_facteur[n+1]

        p = p + 1
        print("------------")
        print(p)
        est_premier = rabbin_miller_boucle(p)
    print(p_facteur)
    return p, p_facteur
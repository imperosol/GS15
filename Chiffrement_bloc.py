'''
Pour la génération de sous-clé de Feistel, on divise la clé d'entrée en N sous-clés.
La taille de la sous-clé correspond à la taille du bloc à chiffrer

PISTE AMELIORATION : Hasher la clé pour qu'elle soit plus petite
'''
# TODO Faire en sorte que

NBR_TOURNE_FEISTEL: int = 32


def bourrage_zero(nbr_bin: str, taille: int) -> str:
    bourrage: str = ""
    for i in range(len(nbr_bin), taille):
        bourrage = bourrage + "0"
    nbr_bin = bourrage + nbr_bin
    return nbr_bin

def fonction_feistel(d:int, cle:int, taille_cle) -> int:
    '''
    F(d, sous_cle) = d + sous_cle mod taille_cle
    '''

    resultat = (d + cle) % pow(2,taille_cle)
    return resultat

def decalage_cle_feistel(cle:int,taille_cle:int) -> int:
    cle_bin = format(cle, "b")
    cle_bin = bourrage_zero(cle_bin,taille_cle)
    cle_bin = cle_bin[2:] + cle_bin[:2]

    resultat = int(cle_bin,2)
    return resultat

def tournee_feistel_chiffrement(d_1:int, g_1:int, cle:int, taille_cle:int) -> (int, int):
    g_2: int = d_1
    d_2: int = g_1 ^ fonction_feistel(d_1, cle, taille_cle)

    cle = decalage_cle_feistel(cle, taille_cle)
    # print(fonction_feistel(g_1, cle, taille_cle))
    # print(cle)
    return d_2, g_2, cle

def tournee_feistel_dechiffrement(d_1:int, g_1:int, cle:int, taille_cle:int) -> (int, int):
    d_2: int = g_1
    g_2: int = d_1 ^ fonction_feistel(g_1, cle, taille_cle)

    cle_bin = format(cle, "b")
    cle_bin = bourrage_zero(cle_bin, taille_cle)
    cle_bin = cle_bin[taille_cle-2:] + cle_bin[:taille_cle-2]
    cle = int(cle_bin, 2)

    return d_2, g_2, cle

def feistel_preparation_dg(nbr: int, taille_cle: int) -> (int, int, list):
    nbr_bin = bourrage_zero(format(nbr, "b"), taille_cle*2)
    print(len(nbr_bin))
    print(nbr_bin)
    d = int(nbr_bin[:(taille_cle)], 2)
    if len(nbr_bin) <= taille_cle:
        g = 0
    else:
        g = int(nbr_bin[(taille_cle):], 2)

    return d, g

def feistel_chiffrement(nbr: int, cle: int, taille_cle: int, nb_tournee) -> int:
    d, g = feistel_preparation_dg(nbr, taille_cle)
    for i in range(nb_tournee):
        d, g, cle = tournee_feistel_chiffrement(d, g, cle, taille_cle)

    d_bin = bourrage_zero(format(d, "b"), taille_cle)
    g_bin = bourrage_zero(format(g, "b"), taille_cle)

    resultat = d_bin + g_bin
    print(resultat)
    return resultat

def feistel_dechiffrement(nbr: int, cle: int, taille_cle: int, nb_tournee) -> int:
    d, g = feistel_preparation_dg(nbr, taille_cle)

    for i in range(nb_tournee - 1):
        cle = decalage_cle_feistel(cle, taille_cle)

    for i in range(nb_tournee):
        d, g, cle = tournee_feistel_dechiffrement(d, g, cle, taille_cle)

    d_bin = bourrage_zero(format(d, "b"), taille_cle)
    g_bin = bourrage_zero(format(g, "b"), taille_cle)

    resultat = d_bin + g_bin
    return resultat

def division_message_bloc(message: str, taille_cle) -> (list, int):

    message_divise: list = list()
    taille_message = len(message)
    nbrdivision = taille_message // (taille_cle * 2)

    if taille_message % (taille_cle*2) != 0:
        nbrdivision += 1

    print(taille_message)
    print(nbrdivision)
    for i in range(nbrdivision):
        message_divise.append(int(message[taille_cle * 2 * i:taille_cle * 2 *(i+1)], 2))

    return message_divise, nbrdivision

def chiffrement_bloc(message:str, cle:int, taille_cle:int) -> str:
    '''
    Divise le message binaire en N sous blocs de 2048 bits
    CHiffre chacun de ces blocs à l'aide d'un schéma à 32 tournées de Feistel
    '''

    message_divise, nbr_division = division_message_bloc(message,taille_cle)
    print("nbr à chiffrer :",int(message,2))
    message_chiffre:str = ""
    for i in range(nbr_division):
        message_chiffre_partiel = feistel_chiffrement(message_divise[i], cle, taille_cle, NBR_TOURNE_FEISTEL)
        if len(message[taille_cle*2*i:]) < taille_cle*2:
            message_chiffre_partiel = message_chiffre_partiel[(taille_cle-len(message[taille_cle*2*i:])):]
        message_chiffre += message_chiffre_partiel
    return message_chiffre

def dechiffrement_bloc(message:str, cle:int, taille_cle:int) -> str:
    '''
    Divise le message binaire en N sous blocs de 2048 bits
    CHiffre chacun de ces blocs à l'aide d'un schéma à 32 tournées de Feistel
    '''

    message_divise, nbr_division = division_message_bloc(message,taille_cle)
    message_dechiffre:str = ""
    for i in range(nbr_division):
        message_dechiffre_partiel = feistel_dechiffrement(message_divise[i], cle, taille_cle, NBR_TOURNE_FEISTEL)
        if len(message[taille_cle*2*i:]) < taille_cle*2:
            message_dechiffre_partiel = message_dechiffre_partiel[(taille_cle-len(message[taille_cle*2*i:])):]
        message_dechiffre += message_dechiffre_partiel
    return message_dechiffre


cle_globale = int("1000101000", 2)
message = "100111011101100110001100111000011111110001111000111000000011101111000001000110101010100101010111110010100"

message_chiffre = chiffrement_bloc(message, cle_globale, 10)
print(message_chiffre)
print(("-DECHIFFREMENT-"))
message_dechiffre = dechiffrement_bloc(message_chiffre, cle_globale, 10)
print(message_dechiffre)
from .Fonctions import bourrage_zero
'''
Pour la génération de sous-clé de Feistel, on divise la clé d'entrée en N sous-clés.
La taille de la sous-clé correspond à la taille du bloc à chiffrer

PISTE AMELIORATION : Hasher la clé pour qu'elle soit plus petite
'''
NBR_TOURNE_FEISTEL: int = 32


def fonction_feistel(d: int, cle: int, taille_cle) -> int:
    '''
    applique la fonction de Festel
    F(d, cle) = d + cle mod taille_cle
    '''

    resultat = (d + cle) % pow(2, taille_cle)
    return resultat


def decalage_cle_feistel(cle: int, taille_cle: int) -> int:
    """
    Calcul la clé n+1 à partir de la clé n
    clé(n+1) = ddéclage de 2 bits vers la gauche de clé(n)
    """

    cle_bin = format(cle, "b")
    cle_bin = bourrage_zero(cle_bin, taille_cle)
    cle_bin = cle_bin[2:] + cle_bin[:2]

    resultat = int(cle_bin, 2)
    return resultat


def tournee_feistel_chiffrement(d_1: int, g_1: int, cle: int, taille_cle: int) -> (int, int):
    """
    Applique une tournée de chiffrement de Feistel
    """

    g_2: int = d_1
    d_2: int = g_1 ^ fonction_feistel(d_1, cle, taille_cle)

    cle = decalage_cle_feistel(cle, taille_cle)

    return d_2, g_2, cle


def tournee_feistel_dechiffrement(d_1: int, g_1: int, cle: int, taille_cle: int) -> (int, int):
    """
    Applique une tournée de déchiffrement de Feistel
    """

    d_2: int = g_1
    g_2: int = d_1 ^ fonction_feistel(g_1, cle, taille_cle)

    # Fonction inverse de décalage de clé
    cle_bin = format(cle, "b")
    cle_bin = bourrage_zero(cle_bin, taille_cle)
    cle_bin = cle_bin[taille_cle - 2:] + cle_bin[:taille_cle - 2]
    cle = int(cle_bin, 2)

    return d_2, g_2, cle


def feistel_preparation_dg(nbr: int, taille_cle: int) -> (int, int):
    '''
    Calcul les D0 et G0 d'un nombre nbr pour initialiser les tournées de Feistel
    '''

    # Fait en sorte que nbr_bin ait la longueur de taille_cle * 2
    nbr_bin = bourrage_zero(format(nbr, "b"), taille_cle * 2)

    d = int(nbr_bin[:(taille_cle)], 2)

    if len(nbr_bin) <= taille_cle:
        g = 0
    else:
        g = int(nbr_bin[(taille_cle):], 2)

    return d, g


def feistel_chiffrement(nbr: int, cle: int, taille_cle: int) -> str:
    """
    Chiffre un nombre nbr avec un clé initiale cle sur un schéma à NBR_TOURNE_FEISTEL
    """

    d, g = feistel_preparation_dg(nbr, taille_cle)

    for i in range(NBR_TOURNE_FEISTEL):
        d, g, cle = tournee_feistel_chiffrement(d, g, cle, taille_cle)

    # Augmente la taille de d_bin et g_bin à taille_cle pour que la fusion des deux donne le nombre voulu
    d_bin = bourrage_zero(format(d, "b"), taille_cle)
    g_bin = bourrage_zero(format(g, "b"), taille_cle)

    resultat = d_bin + g_bin
    return resultat

def feistel_dechiffrement(nbr: int, cle: int, taille_cle: int) -> int:
    """
    Déchiffre un nombre nbr avec un clé initiale cle sur un schéma à NBR_TOURNE_FEISTEL
    """
    d, g = feistel_preparation_dg(nbr, taille_cle)

    # initialisation de la valeur de la clé
    for i in range(NBR_TOURNE_FEISTEL - 1):
        cle = decalage_cle_feistel(cle, taille_cle)

    for i in range(NBR_TOURNE_FEISTEL):
        d, g, cle = tournee_feistel_dechiffrement(d, g, cle, taille_cle)

    # Augmente la taille de d_bin et g_bin à taille_cle pour que la fusion des deux donne le nombre voulu
    d_bin = bourrage_zero(format(d, "b"), taille_cle)
    g_bin = bourrage_zero(format(g, "b"), taille_cle)

    resultat = d_bin + g_bin
    return resultat


def division_message_bloc(message: str, taille_cle) -> (list, int):
    """
    Divise un message en nbr_division bloc de taille taille_cle*2

    retourne le nombre de bloc et une liste avec les messages divisés
    """
    message_divise: list = list()
    taille_message = len(message)
    nbr_division = taille_message // (taille_cle * 2)

    if taille_message % (taille_cle * 2) != 0:
        nbr_division += 1

    for i in range(nbr_division):
        message_divise.append(int(message[taille_cle * 2 * i:taille_cle * 2 * (i + 1)], 2))

    return message_divise, nbr_division


def chiffrement_bloc(message: str, cle: int, taille_cle: int) -> str:
    '''
    Divise le message binaire en nbr_division sous blocs de taille_cle bits
    CHiffre chacun de ces blocs à l'aide d'un schéma à NBR_TOURNE_FEISTEL tournées de Feistel
    '''

    # Divise un message en nbr_division bloc de taille taille_cle*2
    message_divise, nbr_division = division_message_bloc(message, taille_cle)
    message_chiffre: str = ""

    for i in range(nbr_division):
        message_chiffre_partiel = feistel_chiffrement(message_divise[i], cle, taille_cle)
        if len(message[taille_cle * 2 * i:]) < taille_cle * 2:
            message_chiffre_partiel = message_chiffre_partiel[(taille_cle - len(message[taille_cle * 2 * i:])):]
        message_chiffre += message_chiffre_partiel
    return message_chiffre


def dechiffrement_bloc(message: str, cle: int, taille_cle: int) -> str:
    '''
    Divise le message binaire en N sous blocs de 2048 bits
    CHiffre chacun de ces blocs à l'aide d'un schéma à 32 tournées de Feistel
    '''

    # Divise un message en nbr_division bloc de taille taille_cle*2
    message_divise, nbr_division = division_message_bloc(message, taille_cle)
    message_dechiffre: str = ""

    for i in range(nbr_division):
        message_dechiffre_partiel = feistel_dechiffrement(message_divise[i], cle, taille_cle)
        if len(message[taille_cle * 2 * i:]) < taille_cle * 2:
            message_dechiffre_partiel = message_dechiffre_partiel[(taille_cle - len(message[taille_cle * 2 * i:])):]
        message_dechiffre += message_dechiffre_partiel
    return message_dechiffre

from .Fonctions import bourrage_zero, exponentiation_rapide
from .Chiffrement_bloc import chiffrement_bloc, dechiffrement_bloc
from .Cle_Ratchet import Cle_Ratchet
from .Cle import Cle
from .RSA import verification_rsa
import random


class Utilisateur:
    sk: int
    cle_ratchet: Cle_Ratchet

    def __init__(self, p, g, nb_cle_otk, name):
        """
        Initialise les valeur des clés pour un utilisateur
        """
        self.id = Cle(p, g)  # Clé preuve pour une utilisation long terme
        self.pk = Cle(p, g)  # pré-clé signée
        self.otpk = []  # jeu de one time pre-clés
        self.nb_cle_otpk = nb_cle_otk  # nombre de one time pre-clés
        self.eph = Cle(p, g)  # Clé éphémère
        self.name = name  # nom de l'utilisateur

        self.pk.signature()

        for i in range(nb_cle_otk):
            self.otpk.append(Cle(p, g))

    def publication_cle(self):
        """
        publications des clés pour le protocole X3DH
        ID publique, pk publique, optk publique (et son indice i)
        """
        i: int = random.randint(0, self.nb_cle_otpk - 1)
        optk: Cle = self.otpk[i]
        return self.id.id_pub, self.pk.id_pub, self.pk.id_pub_signature, self.pk.id_pub_signature_e, self.pk.id_pub_signature_n, optk.id_pub, i

    def calcul_sk_emetteur_x3dh(self, id_a: int, pk_a: int, pk_signature: int, pk_signature_e: int, pk_signature_n: int,
                                otpk_a: int, i: int, p: int, g: int):
        """
        Calcul de la clé partagée SK pour l'emetteur
        """
        pk_a_signature = pk_a % (pow(2, 1024))

        # vérification de la signature
        signature_valide = verification_rsa(pk_signature, pk_a_signature, pk_signature_e, pk_signature_n)
        if signature_valide:
            print("Signature RSA de la pré clé valide")
        else:
            print("Signature RSA de la pré clé invalide")

        self.eph = Cle(p, g)

        # caclul de dh1, dh2, dh3, dh4 puis de sk
        dh1: int = exponentiation_rapide(pk_a, self.id.id_priv, p)
        dh2: int = exponentiation_rapide(id_a, self.eph.id_priv, p)
        dh3: int = exponentiation_rapide(pk_a, self.eph.id_priv, p)
        dh4: int = exponentiation_rapide(otpk_a, self.eph.id_priv, p)
        self.sk = (dh1 + dh2 + dh3 + dh4) % p

        # initialisation de la clé Ratchet
        self.cle_ratchet = Cle_Ratchet(self.sk)

        return self.id.id_pub, self.eph.id_pub, i

    def calcul_sk_recepteur_x3dh(self, id_pub_b, eph_pub_b, i: int, p: int):
        """
        Calcul de la clé partagée SK pour le recepteur
        """
        otpk: Cle = self.otpk[i]

        # caclul de dh1, dh2, dh3, dh4 puis de sk
        dh1: int = exponentiation_rapide(id_pub_b, self.pk.id_priv, p)
        dh2: int = exponentiation_rapide(eph_pub_b, self.id.id_priv, p)
        dh3: int = exponentiation_rapide(eph_pub_b, self.pk.id_priv, p)
        dh4: int = exponentiation_rapide(eph_pub_b, otpk.id_priv, p)

        # initialisation de la clé Ratchet
        self.sk = (dh1 + dh2 + dh3 + dh4) % p

        self.cle_ratchet = Cle_Ratchet(self.sk)

    def publication_cle_dh(self) -> str:
        """
        Publication de la clé publique pour le protocole de Diffie Hellman
        chiffrement et envoie de la clé publique
        """
        self.kdf_ratchet()
        eph_pub_r_bin = chiffrement_bloc(format(self.eph.id_pub, "b"), self.cle_ratchet.cle_message,
                                         self.cle_ratchet.MAX_BYTES)

        return eph_pub_r_bin

    def calcul_rachet_emetteur_dh(self, eph_pub_r_bin: str, p: int, g: int) -> str:
        """
        Calcul de la clé sk pour le protocole de Diffie Hellman
        déchiffrement de la clé publique du recepteur
        CHiffrement et envoie de la clé publique de l'emetteur
        """

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # déchiffrement de la clé publique
        eph_pub_r = int(dechiffrement_bloc(eph_pub_r_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES), 2)

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()
        cle_message = self.cle_ratchet.cle_message

        # création de la nouvelle clé Ratchet
        self.cle_ratchet = Cle_Ratchet(exponentiation_rapide(eph_pub_r, self.eph.id_priv, p))

        # Chiffrement de clé publique par la dernière clé de message calculée (pour qu'elle soit déchiffrable par le recepteur)
        eph_pub_e = chiffrement_bloc(format(self.eph.id_pub, "b"), cle_message, self.cle_ratchet.MAX_BYTES)

        # mise à jour de la clé éphémère
        self.eph = Cle(p, g)

        return eph_pub_e

    def calcul_rachet_recepteur_dh(self, eph_pub_e_bin: str, p: int, g: int):
        """
        Calcul de la clé sk pour le protocole de Diffie Hellman
        déchiffrement du message reçu et chiffrement du message
        """

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # déchiffrement de la clé publique
        eph_pub_e = int(dechiffrement_bloc(eph_pub_e_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES), 2)

        # création de la nouvelle clé Ratchet
        self.cle_ratchet = Cle_Ratchet(exponentiation_rapide(eph_pub_e, self.eph.id_priv, p))

        # mise à jour de la clé éphémère
        self.eph = Cle(p, g)

    def kdf_ratchet(self):
        """
        Appelle la fonction de dérivation d'une clé Ratchet
        """

        self.cle_ratchet.fonction_derivation()

    def envoie_message(self, message: str) -> str:
        """
        Convertit une chaine de caractère en binaire puis la chiffre par un chiffrement par bloc
        Ne convertit que les caractère ASCII, les caractères spéciaux corrompent le message
        """

        # Convertit une chaine de caractère en binaire
        message_bin = ''.join(bourrage_zero(format(ord(i), 'b'), 7) for i in message)

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # Chiffrement du message
        message_chiffre = chiffrement_bloc(message_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES)

        return message_chiffre

    def reception_message(self, message_chiffre) -> str:
        """
        Déchiffre une chaine de caractère en binaire puis la convertit en une chaine de caractère
        Ne convertit que les caractère ASCII, les caractères spéciaux corrompent le message
        """

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # déchiffrement du message
        message_dechiffre = dechiffrement_bloc(message_chiffre, self.cle_ratchet.cle_message,
                                               self.cle_ratchet.MAX_BYTES)

        # Convertit une chaine binaire en chaine de caractère
        message = ''.join(chr(int(message_dechiffre[x * 7:x * 7 + 7], 2)) for x in range(len(message_dechiffre) // 7))

        return message

    def envoie_fichier(self, chemin_fichier: str):

        with open(chemin_fichier) as file:
            fichier = file.read()

            # On convertit chaque caractère en décimal puis en binaire
            message_bin = ''.join(bourrage_zero(format(ord(x), 'b'), 7) for x in fichier)

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # Chiffrement du message
        message_chiffre = chiffrement_bloc(message_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES)

        return message_chiffre

    def reception_fichier(self, message_chiffre: str):

        # incrémentation de la clé Ratchet
        self.kdf_ratchet()

        # déchiffrement du message
        message_dechiffre = dechiffrement_bloc(message_chiffre, self.cle_ratchet.cle_message,
                                               self.cle_ratchet.MAX_BYTES)

        fichier_donne = ''.join(
            chr(int(message_dechiffre[x * 7:x * 7 + 7], 2)) for x in range(len(message_dechiffre) // 7))
        with open("./FichierRecu.txt", "w") as fileR:
            fileR.write(fichier_donne)

from .Fonctions import bourrage_zero, exponentiation_rapide
from .Chiffrement_bloc import chiffrement_bloc, dechiffrement_bloc
from .Cle_Ratchet import Cle_Ratchet
from .Cle import Cle
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
        self.otpk = [] # jeu de one time pre-clés
        self.nb_cle_otpk = nb_cle_otk # nombre de one time pre-clés
        self.eph = Cle(p, g)  # Clé éphémère
        self.name = name # nom de l'utilisateur

        # self.pk.signature() TODO ecrire la fonction de signature

        for i in range(nb_cle_otk):
            self.otpk.append(Cle(p, g))

    def publication_cle(self):
        i: int = random.randint(0, self.nb_cle_otpk - 1)
        optk: Cle = self.otpk[i]
        return self.id.id_pub, self.pk.id_pub, optk.id_pub, i

    def calcul_sk_emetteur_x3dh(self, id_a: int, pk_a: int, otpk_a: int, i: int, p: int, g: int):
        """
        Calcul de la clé partagée SK pour Bob
        """
        # TODO : vérification de la signature ajouter sig_pk_a: int auix paramètres
        self.eph = Cle(p, g)

        dh1: int = exponentiation_rapide(pk_a, self.id.id_priv, p)
        dh2: int = exponentiation_rapide(id_a, self.eph.id_priv, p)
        dh3: int = exponentiation_rapide(pk_a, self.eph.id_priv, p)
        dh4: int = exponentiation_rapide(otpk_a, self.eph.id_priv, p)

        self.sk = (dh1 + dh2 + dh3 + dh4) % p

        self.cle_ratchet = Cle_Ratchet(self.sk)

        return self.id.id_pub, self.eph.id_pub, i

    def calcul_sk_destinataire_x3dh(self, id_pub_b, eph_pub_b, i: int, p: int):
        otpk: Cle = self.otpk[i]
        dh1: int = exponentiation_rapide(id_pub_b, self.pk.id_priv, p)
        dh2: int = exponentiation_rapide(eph_pub_b, self.id.id_priv, p)
        dh3: int = exponentiation_rapide(eph_pub_b, self.pk.id_priv, p)
        dh4: int = exponentiation_rapide(eph_pub_b, otpk.id_priv, p)

        self.sk = (dh1 + dh2 + dh3 + dh4) % p  # TODO définir la fonction de calcul

        self.cle_ratchet = Cle_Ratchet(self.sk)

    def publication_cle_dh(self) -> str:
        self.kdf_ratchet()
        eph_pub_r_bin = chiffrement_bloc(format(self.eph.id_pub, "b"), self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES)
        print("Clé éphémère publique recepteur")
        print("recepteur :", format(self.eph.id_pub, "b"))

        return eph_pub_r_bin



    def calcul_rachet_emetteur_dh(self, eph_pub_r_bin: str, p: int, g: int) -> str:
        self.kdf_ratchet()
        eph_pub_r = int(dechiffrement_bloc(eph_pub_r_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES), 2)


        self.kdf_ratchet()
        cle_message = self.cle_ratchet.cle_message

        self.cle_ratchet = Cle_Ratchet(exponentiation_rapide(eph_pub_r, self.eph.id_priv, p))
        eph_pub_e = chiffrement_bloc(format(self.eph.id_pub, "b"), cle_message, self.cle_ratchet.MAX_BYTES)
        self.eph = Cle(p, g)

        return eph_pub_e

    def calcul_rachet_recepteur_dh(self, eph_pub_e_bin: str, p: int, g: int):
        self.kdf_ratchet()

        eph_pub_e = int(dechiffrement_bloc(eph_pub_e_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES), 2)

        self.cle_ratchet = Cle_Ratchet(exponentiation_rapide(eph_pub_e, self.eph.id_priv, p))
        self.eph = Cle(p, g)

    def kdf_ratchet(self):
        self.cle_ratchet.fonction_derivation()

    def envoie_message(self, message: str) -> str:
        # message_bin = ''.join(format(ord(x), 'b') for x in message)
        message_bin = ''.join(bourrage_zero(format(ord(i), 'b'), 7) for i in message)
        print(message_bin)
        self.kdf_ratchet()
        message_chiffre = chiffrement_bloc(message_bin, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES)

        return message_chiffre

    def reception_message(self, message_chiffre) -> str:
        self.kdf_ratchet()

        message_dechiffre = dechiffrement_bloc(message_chiffre, self.cle_ratchet.cle_message, self.cle_ratchet.MAX_BYTES)
        print(message_dechiffre)
        message = ''.join(chr(int(message_dechiffre[x*7:x*7+7], 2)) for x in range(len(message_dechiffre)//7))

        return message


'''
Mise à jour de la clé partagée via Diffie Hellman, une seule clé suffit

Envoie "classique de message" de Bob à Alice

Bob calcul une nouvelle clé
'''

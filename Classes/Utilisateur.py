from Cle import Cle
from Cle_Rachet import Cle_Rachet
import Fonctions
import random


class Utilisateur:
    # TODO : créer une paire de clé Rachet

    sk: int
    cle_rachet : Cle_Rachet


    def __init__(self, p, g, nb_cle_otk):
        self.id = Cle(p, g)  # Clé preuve pour une utilisation long terme
        self.pk = Cle(p, g)  # pré-clé signée
        self.otpk = []
        self.nb_cle_otpk = nb_cle_otk
        self.eph = Cle(p, g) # Clé éphémère
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



        dh1: int = Fonctions.exponentiation_rapide(pk_a, self.id.id_priv, p)
        dh2: int = Fonctions.exponentiation_rapide(id_a, self.eph.id_priv, p)
        dh3: int = Fonctions.exponentiation_rapide(pk_a, self.eph.id_priv, p)
        dh4: int = Fonctions.exponentiation_rapide(otpk_a, self.eph.id_priv, p)

        self.sk = dh1 | dh2 | dh3 | dh4  # TODO définir la fonction de calcul

        self.eph = Cle(p, g)
        self.cle_rachet = Cle_Rachet(self.sk)

        return self.id.id_pub, eph.id_pub, i

    def calcul_sk_destinataire_x3dh(self, id_pub_b, eph_pub_b, i: int, p: int):
        otpk: Cle = self.otpk[i]
        dh1: int = Fonctions.exponentiation_rapide(id_pub_b, self.pk.id_priv, p)
        dh2: int = Fonctions.exponentiation_rapide(eph_pub_b, self.id.id_priv, p)
        dh3: int = Fonctions.exponentiation_rapide(eph_pub_b, self.pk.id_priv, p)
        dh4: int = Fonctions.exponentiation_rapide(eph_pub_b, otpk.id_priv, p)

        self.cle_rachet = Cle_Rachet(self.sk)

        self.sk = dh1 | dh2 | dh3 | dh4  # TODO définir la fonction de calcul

    def publication_cle_dh(self):
        return self.eph.id_pub()

    def calcul_rachet_emetteur_dh(self, eph_pub_r:int, p: int, g: int) -> int:

        self.cle_rachet = Cle_Rachet(Fonctions.exponentiation_rapide(eph_pub_r, self.eph.id_priv, p))

        eph_pub_e = self.eph.id_pub()
        self.eph = Cle(p, g)

        return eph_pub_e

    def calcul_rachet_recepteur_dh(self, eph_pub_e:int, p: int, g: int):

        self.cle_rachet = Cle_Rachet(Fonctions.exponentiation_rapide(eph_pub_e, self.eph.id_priv, p))
        self.eph = Cle(p, g)


'''
Mise à jour de la clé partagée via Diffie Hellman, une seule clé suffit

Envoie "classique de message" de Bob à Alice

Bob calcul une nouvelle clé


'''
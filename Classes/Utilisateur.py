from Cle import Cle
import Fonctions
import random


class Utilisateur:
    sk: int

    def __init__(self, p, g, nb_cle_otk):
        self.id = Cle(p, g)  # Clé preuve pour une utilisation long terme
        self.pk = Cle(p, g)  # pré-clé signée
        self.otpk = []
        self.nb_cle_otpk = nb_cle_otk
        # self.pk.signature() TODO ecrire la fonction de signature
        for i in range(nb_cle_otk):
            self.otpk.append(Cle(p, g))

    def publication_cle(self):
        i: int = random.randint(0, self.nb_cle_otpk - 1)
        optk: Cle = self.otpk[i]
        return self.id.id_pub, self.pk.id_pub, optk.id_pub, i

    def calcul_sk_bob(self, id_a: int, pk_a: int, otpk_a: int, i: int, p: int, g: int):
        """
        Calcul de la clé partagée SK pour Bob
        """
        # TODO : vérification de la signature ajouter sig_pk_a: int auix paramètres

        eph: Cle = Cle(p, g)

        dh1: int = Fonctions.exponentiation_rapide(pk_a, self.id.id_priv, p)
        dh2: int = Fonctions.exponentiation_rapide(id_a, eph.id_priv, p)
        dh3: int = Fonctions.exponentiation_rapide(pk_a, eph.id_priv, p)
        dh4: int = Fonctions.exponentiation_rapide(otpk_a, eph.id_priv, p)
        self.sk = dh1 | dh2 | dh3 | dh4
        return self.id.id_pub, eph.id_pub, i

    def calcul_sk_alice(self, id_pub_b, eph_pub_b, i: int, p: int):
        otpk: Cle = self.otpk[i]
        dh1: int = Fonctions.exponentiation_rapide(id_pub_b, self.pk.id_priv, p)
        dh2: int = Fonctions.exponentiation_rapide(eph_pub_b, self.id.id_priv, p)
        dh3: int = Fonctions.exponentiation_rapide(eph_pub_b, self.pk.id_priv, p)
        dh4: int = Fonctions.exponentiation_rapide(eph_pub_b, otpk.id_priv, p)

        self.sk = dh1 | dh2 | dh3 | dh4

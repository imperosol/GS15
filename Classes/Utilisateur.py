from GS15.Classes.Cle import Cle
import Fonctions
import random


class Utilisateur:
    id: Cle  # Clé préuve pour une utilisation long terme
    pk: Cle  # pré-clé signée
    otpk: list[Cle]  # liste de clés utilisable une fois
    nb_cle_otpk: int  # Nombre de clés optk disponibles

    sk: int

    def __init__(self, p, g, nb_cle_otk):
        self.id = Cle(p, g)
        self.pk = Cle(p, g)
        self.otpk = list()
        self.nb_cle_otpk = nb_cle_otk
        # self.pk.signature() TODO ecrire la fonction de signature
        for i in range(nb_cle_otk):
            self.otpk.append(Cle(p, g))

    def publication_cle(self):
        i: int = random.randint(0, self.nb_cle_otpk - 1)
        optk: Cle = self.otpk[i]
        return self.id.get_id_pub(), self.pk.get_id_pub(), optk.get_id_pub(), i

    def calcul_sk_bob(self, id_a: int, pk_a: int, otpk_a: int, i: int, p: int, g: int):
        '''Calcul de la clé partagée SK pour Bob'''
        # TODO : vérification de la signature ajouter sig_pk_a: int auix paramètres

        eph: Cle = Cle(p, g)

        dh1: int = Fonctions.exponentiation_rapide(pk_a, self.id.get_id_priv(), p)
        dh2: int = Fonctions.exponentiation_rapide(id_a, eph.get_id_priv(), p)
        dh3: int = Fonctions.exponentiation_rapide(pk_a, eph.get_id_priv(), p)
        dh4: int = Fonctions.exponentiation_rapide(otpk_a, eph.get_id_priv(), p)

        self.sk = dh1 | dh2 | dh3 | dh4

        print("Bob")
        print("DH1 =", dh1)
        print("DH2 =", dh2)
        print("DH3 =", dh3)
        print("DH4 =", dh4)
        print("SK =", self.sk)
        print("-------------")

        return self.id.get_id_pub(), eph.get_id_pub(), i

    def calcul_sk_alice(self, id_pub_b, eph_pub_b, i: int, p: int):
        otpk: Cle = self.otpk[i]
        dh1: int = Fonctions.exponentiation_rapide(id_pub_b, self.pk.get_id_priv(), p)
        dh2: int = Fonctions.exponentiation_rapide(eph_pub_b, self.id.get_id_priv(), p)
        dh3: int = Fonctions.exponentiation_rapide(eph_pub_b, self.pk.get_id_priv(), p)
        dh4: int = Fonctions.exponentiation_rapide(eph_pub_b, otpk.get_id_priv(), p)

        self.sk = dh1 | dh2 | dh3 | dh4

        print("Alice")
        print("DH1 =", dh1)
        print("DH2 =", dh2)
        print("DH3 =", dh3)
        print("DH4 =", dh4)
        print("SK =", self.sk)
        print("-------------")

import random
import numpy as np
import Fonctions
import RSA


class Cle:
    p: int  # nombre premier
    g: int  # élément générateur de Zp
    max: int = 2048
    id_pub: int  # clé publique ( g ^ id_priv mod p)
    id_priv: int  # clé privée
    sig: int  # Signature de la clé publique

    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.id_priv = random.randint(1, self.max)
        self.id_pub = Fonctions.exponentiation_rapide(self.g, self.id_priv, self.p)

        # TODO : Signature de la pré-clé
        # self.signature(self)

    def __int__(self, id_pub, id_priv, sig_pk_pub, sig_sig_pk_pub):
        self.id_pub = id_pub
        self.id_priv = id_priv
        self.sig_pk_pub = sig_pk_pub
        self.sig_sig_pk_pub = sig_sig_pk_pub

    def get_id_pub(self) -> int:
        return self.id_pub

    def get_id_priv(self) -> int:
        return self.id_priv

    def get_sig(self) -> int:
        return self.sig

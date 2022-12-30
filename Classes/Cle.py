import random
from Fonctions import exponentiation_rapide


class Cle:
    MAX_BYTES: int = 2048

    def __init__(self, p, g):
        self._id_priv = random.randint(1, Cle.MAX_BYTES)
        self._id_pub = exponentiation_rapide(g, self._id_priv, p)
        self._pub_key_signature = 0

        # TODO : Signature de la pré-clé
        # self.signature(self)

    def __int__(self, id_pub, id_priv, sig_pk_pub, sig_sig_pk_pub):
        self._id_pub = id_pub
        self._id_priv = id_priv
        self.sig_pk_pub = sig_pk_pub
        self.sig_sig_pk_pub = sig_sig_pk_pub

    @property
    def id_pub(self) -> int:
        return self._id_pub

    @property
    def id_priv(self) -> int:
        return self._id_priv

    @property
    def pub_key_signature(self) -> int:
        return self.pub_key_signature

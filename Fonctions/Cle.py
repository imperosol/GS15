import random
from .Fonctions import exponentiation_rapide
from Fonctions.RSA import signature_rsa


class Cle:
    """
    Stock la clé publique, la clé privée et la signature d'une clée
    """
    MAX_BYTES: int = 2048

    def __init__(self, p, g):
        self._id_priv = random.randint(1, Cle.MAX_BYTES)
        self._id_pub = exponentiation_rapide(g, self._id_priv, p)
        self._id_pub_signature = 0
        self._id_pub_signature_n = 0
        self._id_pub_signature_e = 0


    def signature(self):
        """
        On ne signe les 1024 premiers bits de la clé via RSA
        """
        id_pub_a_signer = self.id_pub % pow(2, 1024)
        self._id_pub_signature, self._id_pub_signature_e, self._id_pub_signature_n = signature_rsa(id_pub_a_signer)

    @property
    def id_pub(self) -> int:
        return self._id_pub

    @property
    def id_priv(self) -> int:
        return self._id_priv

    @property
    def id_pub_signature(self) -> int:
        return self._id_pub_signature

    @property
    def id_pub_signature_n(self) ->int:
        return self._id_pub_signature_n

    @property
    def id_pub_signature_e(self) ->int:
        return self._id_pub_signature_e
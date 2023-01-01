from GS15.Classes.Fonctions import exponentiation_rapide

class Cle_Ratchet:

    MAX_BYTES: int = 2048

    def __init__(self, cle_chainee):
        self._cle_chainee = cle_chainee
        self._cle_message = 0

    def fonction_derivation(self):
        """

        cle_chainee(n + 1) = cle_chainee(n) * cle_chainee(n)
        cle_message(n + 1) = cle_chainee(n) * cle_chainee(n + 1)

        """
        # print(self._cle_chainee)
        cle_chainee_suivante = self._cle_chainee * self._cle_chainee % pow(2, self.MAX_BYTES)

        self._cle_message = cle_chainee_suivante * self._cle_chainee % pow(2, self.MAX_BYTES)
        # print(self._cle_message)
        self._cle_chainee = cle_chainee_suivante

    @property
    def cle_message(self):
        return self._cle_message

    @property
    def cle_chainee(self):
        return self._cle_chainee


'''
Clé symétrique Rachet mise à jour régulièrement



'''

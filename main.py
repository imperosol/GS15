from Classes.Utilisateur import Utilisateur

p: int = 201665270259920855767397920814877447408782241119556263250562946574743587126138643687759014887579644968574614550773047679511971903637815898297082341209086681300582289972148613685506069925389324659674924253072250738467392327134096989057363354903644370391721709867648261245817942851683633005181963565130901955691454982900338179115034963414757105798395756048030075018946135754768749404323433116039270920829570773044387968538758083548875367081919104318171216675464471569440461890550460135354511475047724536275087348241485327756583000871688389484112739697559043503
g: int = 164949937651303727260466688774834622420744237060254454598064973946096018563822607644022670775403745977901008159164042388977788206837240745735500551353607108277698153099601450240692541144952893510958616827545499180422797327672095024114757135638313042610607724735020913725407381590361747698562642744347723816523283847855170408310075940059753486020903931392852418818360869294370605706520950816027034979362238195770898014195729183969594440121609638009145282739165724941013769086219243243381518669620665288490969112860868487761501594803219285552949024090409046154


def main():
    nb_cle_otk = 10

    alice = Utilisateur(p, g, nb_cle_otk, "Alice")
    bob = Utilisateur(p, g, nb_cle_otk, "Bob")

    emetteur: Utilisateur = None
    while emetteur is None:
        choix = input("Qui êtes vous ? 1 : Alice, 2 : Bob")
        if choix == '1':
            emetteur = alice
            recepteur = bob
        if choix == '2':
            emetteur = bob
            recepteur = alice
        print(choix)

    # Echange initial de clé entre emetteur et recepteur via X3DH

    id_pub_a, pk_pub_a, optk_pub_a, optk_i = recepteur.publication_cle()
    id_pub_b, id_eph, optk_i = emetteur.calcul_sk_emetteur_x3dh(id_pub_a, pk_pub_a, optk_pub_a, optk_i, p, g)
    recepteur.calcul_sk_destinataire_x3dh(id_pub_b, id_eph, optk_i, p)

    while True:
        print("--------------------------")
        print("Que souhaitez vous faire ?")
        print("1 : comparer la valeur des clés")
        print("2 : incrémenter les clés Rachet")
        print("3 : nouvelles clés via dh")
        choix = input("commande :")

        if choix == '1':
            print("-emetteur-")
            print("clé sk partagée :", emetteur.sk)
            print("clé Ratchet chainée :", emetteur.cle_ratchet.cle_chainee)
            print("")
            print("-recepteur-")
            print("clé sk partagée :", recepteur.sk)
            print("clé Ratchet chainée :", recepteur.cle_ratchet.cle_chainee)
        if choix == '2':
            emetteur.kdf_ratchet()
            recepteur.kdf_ratchet()


if __name__ == '__main__':
    main()



'''
Créer un menu utilisateur permettant de respectivement

- Envoyer un fichier
- Envoyer un message

'''
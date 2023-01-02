from Fonctions.Utilisateur import Utilisateur
from GS15.Fonctions import Fonctions


def main():
    # Le nombre premier p et l'élément générateur de Zp sont fixés pour optimiser le temps d'exécution de l'algorithme
    p: int = 201665270259920855767397920814877447408782241119556263250562946574743587126138643687759014887579644968574614550773047679511971903637815898297082341209086681300582289972148613685506069925389324659674924253072250738467392327134096989057363354903644370391721709867648261245817942851683633005181963565130901955691454982900338179115034963414757105798395756048030075018946135754768749404323433116039270920829570773044387968538758083548875367081919104318171216675464471569440461890550460135354511475047724536275087348241485327756583000871688389484112739697559043503
    g: int = 164949937651303727260466688774834622420744237060254454598064973946096018563822607644022670775403745977901008159164042388977788206837240745735500551353607108277698153099601450240692541144952893510958616827545499180422797327672095024114757135638313042610607724735020913725407381590361747698562642744347723816523283847855170408310075940059753486020903931392852418818360869294370605706520950816027034979362238195770898014195729183969594440121609638009145282739165724941013769086219243243381518669620665288490969112860868487761501594803219285552949024090409046154

    # On fixe le nombre de clés à usage unique stockée dans le serveur
    nb_cle_otk = 10

    # On défini les 2 utilisateurs
    alice = Utilisateur(p, g, nb_cle_otk, "Alice")
    bob = Utilisateur(p, g, nb_cle_otk, "Bob")

    # On défini l'emetteur (ainsi que le récepteur) enfin de déterminer celui qui réalisera l'échange de clé avec le
    # serveur
    emetteur: Utilisateur = None
    while emetteur is None:
        print("Qui êtes vous ? 1 : Alice, 2 : Bob")
        choix = input("")
        if choix == '1':
            emetteur = alice
            recepteur = bob
        elif choix == '2':
            emetteur = bob
            recepteur = alice

    # Echange initial de clé entre emetteur et recepteur via X3DH
    id_pub_a, pk_pub_a, pk_sig, pk_sig_e, pk_sig_n, optk_pub_a, optk_i = recepteur.publication_cle()
    id_pub_b, id_eph, optk_i = emetteur.calcul_sk_emetteur_x3dh(id_pub_a, pk_pub_a, pk_sig, pk_sig_e, pk_sig_n, optk_pub_a, optk_i, p, g)
    recepteur.calcul_sk_recepteur_x3dh(id_pub_b, id_eph, optk_i, p)

    # Menu utilisateur
    continu: bool = True
    while (continu == True):
        print("--------------------------")
        print("Que souhaitez vous faire ?")
        print("1 : comparer la valeur des clés")
        print("2 : incrémenter les clés Rachet")
        print("3 : nouvelles clés via dh")
        print("4 : envoyer un message")
        print("5 : envoyer un fichier")
        print("6 : générer un nombre premier p et un élément générateur de l'ensemble Zp")
        print("7 : quitter")
        choix = input("commande : ")

        # Permet de vérifier que l'émetteur et le récepteur la même clé secrète
        if choix == '1':
            print("-emetteur-")
            print("clé sk partagée : ", emetteur.sk)
            print("clé Ratchet chainée : ", emetteur.cle_ratchet.cle_chainee)
            print("")
            print("-recepteur-")
            print("clé sk partagée : ", recepteur.sk)
            print("clé Ratchet chainée : ", recepteur.cle_ratchet.cle_chainee)

        # Incrémentation des clés Rachet
        elif choix == '2':
            emetteur.kdf_ratchet()
            recepteur.kdf_ratchet()

        # Utilisation de nouvelles clés pour l'échange via Diffie-Hellman
        elif choix == '3':
            eph_pub_r_bin = recepteur.publication_cle_dh()
            eph_pub_e_bin = emetteur.calcul_rachet_emetteur_dh(eph_pub_r_bin, p, g)
            recepteur.calcul_rachet_recepteur_dh(eph_pub_e_bin, p, g)

        # Envoi d'un message texte avec le chiffrement de Feistel
        elif choix == '4':
            print("entrer le message à envoyer (seulement composé de caractères ASCII) ")
            message = input("")
            print("-", emetteur.name, "-")
            message_chiffre = emetteur.envoie_message(message)
            print("message chiffré : ", message_chiffre)
            message_dechiffre = recepteur.reception_message(message_chiffre)
            print("-", recepteur.name, "-")
            print("message déchiffré : ", message_dechiffre)

        # Envoi d'un fichier texte avec le chiffrement de Feistel
        elif choix == '5':
            # Demande à l'utilisateur de sélectionner le fichier
            print("Entrer le chemin absolu du fichier texte à envoyer (seulement composé de caractères ASCII) ")
            chemin_fichier = input("")
            message_chiffre = emetteur.envoie_fichier(chemin_fichier)
            recepteur.reception_fichier(message_chiffre)

        # Permet de montrer que le calcul d'un nombre premier p et un élément générateur de l'ensemble Zp est possible grâce aux fonctions dans le programme
        elif choix == '6':
            bit_max = int(input("nombre de bits du nombre premier :"))
            print("Génération d'un nombre premier p et d'un élément générateur de l'ensemble Zp")
            print("Cette opération peut prendre quelques minutes...")
            p, p_facteur = Fonctions.gen_nbr_premier_produit(bit_max)
            g = Fonctions.generateur_facteur(p, p_facteur)
            print("nombre premier p : ", p)
            print("element générateur de Zp : ", g)
        # Quitter le programme
        elif choix == '7':
            print("Vous quittez le programme")
            continu = False

if __name__ == '__main__':
    main()

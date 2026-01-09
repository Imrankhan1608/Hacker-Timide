from style import banner, clear
import time


# ====== COULEURS TERMINAL ======
BLUE   = "\033[94m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def main():
    # mettre les ip dans une liste et chnages en int
    def iptolist():
        while True:
            ip = input("entrer une adresse : ").strip()
            listring = ip.split(".")
            if len(listring) != 4:
                print("Erreur : une adresse IP doit avoir 4 octets.")
                continue
            try:
                listip = [int(partie) for partie in listring]
                if all(0 <= octet <= 255 for octet in listip):
                    break
                else:
                    print("Erreur : chaque octet doit être entre 0 et 255.")
            except ValueError:
                print("Erreur : chaque octet doit être un nombre entier.")
        
        while True:
            try:
                cidr = int(input("donner le CIDR /X : "))
                if 0 <= cidr <= 32:
                    break
                else:
                    print("Erreur : le CIDR doit être entre 0 et 32.")
            except ValueError:
                print("Erreur : veuillez entrer un nombre entier valide.")
        
        return listip , cidr 


    # changes to binary
    def iptobinary(listip):
        listbinary = []
        for nombre in listip:
            nombrebinaire = format(nombre,"08b")
            listbinary.append(nombrebinaire)
        return listbinary

    # affichage des resultats 
    adress, cidr = iptolist()
    print(f"{CYAN}l'adresse ip est :{RESET}",adress)
    
    adressbinaire = iptobinary(adress)
    print(f"{CYAN}l'adresse en binaire :{RESET}", adressbinaire)

    print(f"{CYAN}CIDR :{RESET}",cidr)
    
    # regrouper les binaires 
    def reseau(listbinary):
        binaire = ""
        for partie in listbinary:
            binaire = str(partie) + binaire
        return binaire

    # affichage du binaire complet
    binaire_complet = reseau(adressbinaire)
    print(f"{CYAN}l'adress en binaire:{RESET}",binaire_complet)

    # detecter le cidr de base selon la classe de l'ip
    def detect_base_cidr(adress):
        premier = adress[0]

        if 1 <= premier <= 126:
            return 8      # classe A
        elif 128 <= premier <= 191:
            return 16     # classe B
        elif 192 <= premier <= 223:
            return 24     # classe C
        else:
            return 32     # cas spécial / sécurité


    # calcul basé sur l'octet actif 
    def calcul_octet_actif(cidr):
        reste = cidr % 8

        if reste == 0:
            bits_octet = 8
        else:
            bits_octet = reste

        masque_octet = 256 - (2 ** (8 - bits_octet))
        pas = 256 - masque_octet
        nombre_sr = 256 // pas

        return masque_octet, nombre_sr

   
    # pour le masque et le sr et les hotes 
    def calculmasque():
        bits_h = 32 - cidr

        # nombre d'hôtes
        if bits_h <= 0:
            nombre_h = 0
        else:
            nombre_h = (2 ** bits_h) - 2

        # calcul via l'octet actif
        masque_octet, nombre_sr = calcul_octet_actif(cidr)

        # génération du masque complet binaire
        liste_stringbits = []

        for _ in range(cidr):
            liste_stringbits.append("1")

        for _ in range(32 - cidr):
            liste_stringbits.append("0")

        valeurf = ''
        for bit in liste_stringbits:
            valeurf += bit

        masque = int(valeurf, 2)

        return nombre_sr, nombre_h, masque
 

    # pour l'affichage du masque, sr , hote
    nb_sr , nb_h , masque_sr= calculmasque()
    print(f"\n{CYAN}{BOLD}--- Informations Réseau ---{RESET}")
    print(f"{GREEN}le nombre de sous reseau :{RESET}",nb_sr)
    print(f"{GREEN}le nombre d'hote disponible :{RESET}",nb_h)


    # pour le format x.x.x.x du masque
    # cette partie est a revoir mais pour l'instant ça marche mdr 
    def affichagemasque(cidr,masque):
        A = (masque >> 24) & 255
        B = (masque >> 16) & 255
        C = (masque >> 8) & 255
        D = masque & 255
        return A, B, C, D


    # chatgpt svp un humain doit le remplacer si c'est possible et le rendre plus lisible
    def afficher_sous_reseaux(adress, cidr, nb_sr):
        """
        Affiche les sous-réseaux pour une IP et un CIDR donnés.
        Utilise le nombre de sous-réseaux déjà calculé.
        """
        ip_int = (adress[0] << 24) | (adress[1] << 16) | (adress[2] << 8) | adress[3]

        # sécuriser le nombre de sous-réseaux à afficher
        while True:
            try:
                n_afficher = int(input(f"Combien de sous-réseaux afficher ? (max {nb_sr}) : "))
                if 1 <= n_afficher <= nb_sr:
                    break
                else:
                    print(f"Erreur : choisissez un nombre entre 1 et {nb_sr}.")
            except ValueError:
                print("Erreur : veuillez entrer un nombre entier valide.")

        # calcul du pas en fonction du nombre de sous-réseaux déjà calculé
        step = 2 ** (32 - cidr)  # pas par sous-réseau

        print(f"\n{CYAN}{BOLD}" + "-"*78)
        print(f"| {'ID':^4} | {'Réseau':^18} | {'Plage Hôtes':^30} | {'Broadcast':^15} |")
        print("-"*78 + f"{RESET}")

        for i in range(n_afficher):
            network_int = ip_int + i * step
            broadcast_int = network_int + step - 1

            # déterminer plage d'hôtes
            if cidr == 31:
                h_start, h_end = network_int, broadcast_int
            elif cidr == 32:
                h_start = h_end = None
            else:
                h_start = network_int + 1
                h_end = broadcast_int - 1

            # conversion entier → IP
            def int_to_ip(x):
                return f"{(x >> 24) & 255}.{(x >> 16) & 255}.{(x >> 8) & 255}.{x & 255}"

            network_ip = int_to_ip(network_int)
            broadcast_ip = int_to_ip(broadcast_int)
            if h_start is not None:
                h_start_ip = int_to_ip(h_start)
                h_end_ip = int_to_ip(h_end)
                plage = f"{h_start_ip} → {h_end_ip}"
            else:
                plage = "Aucun (/32)"

            print(
                f"{BLUE}| {i+1:^4} | "
                f"{GREEN}{network_ip:^18}{BLUE} | "
                f"{WHITE}{plage:^30}{BLUE} | "
                f"{GREEN}{broadcast_ip:^15}{BLUE} |{RESET}"
            )

        print(f"{CYAN}" + "-"*78 + f"{RESET}")


    # affichage du masque 
    octet_1, octet_2, octet_3, octet_4 = affichagemasque(cidr,masque_sr)
    print(f"{GREEN}le masque avec format :{RESET}", octet_1, ".", octet_2, ".", octet_3, ".", octet_4)

    # appel de la fonction pour afficher les sous-réseaux et plages
    afficher_sous_reseaux(adress, cidr, nb_sr)
    


if __name__ == "__main__":
    banner()  # Bannière animée
    input("\nAppuie sur Entrée pour continuer...")
    clear()

    while True:
        # Menu utilisable
        print(f"{CYAN}1 - Lancer le script{RESET}")
        print(f"{CYAN}2 - Actualiser{RESET}")
        print(f"{CYAN}0 - Quitter{RESET}")

        choix = input("\nChoix > ").strip()

        if choix == "0":
            print("Merci pour votre confiance...")
            time.sleep(1)
            break

        elif choix == "2":
            clear()

        elif choix == "1":
            clear()
            main()  #  lancement
            input("\nAppuie sur Entrée pour revenir au menu...")
            clear()

        else:
            print("Choix invalide.")

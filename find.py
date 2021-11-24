# Paramètres qui ont été adaptés d'une manière empirique
seuil=5*10**2
#nb_canaux_max=2  # augmenter ce nombre
nb_canaux_min=1
nb_pas = 6
#pas_bug=4 # paramètre à ajuster

canalmax_mod16=14
canalmax_mod32=26

canalmin_mod16=2
canalmin_mod32=2


def CasdeCharge(dataSort, nb_canaux_max, pas_bug):
    """
    Renvoie une liste de couples indice-instant des cas de charge identifiés.
    Un cas de charge correspond à une succession suffisament longue de dépassement de seuil de count dans un nombre restreint de canaux.
    Afin d'éliminer des cas pathologiques, on requiert que l'indice du/des canaux actifs change au cours de la charge (il arrive qu'un canal bug et reste constamment au dessus du seuil).
    """

    liste_cas=[]

    cas_consec=0
    bug_consec=0

    liste_canaux=[False for i in range(32)]

    for i in dataSort.index:
    # on parcourt la dataframe triée ligne par ligne

        n=0

    # on identifie le mod (16 ou 32 canaux)
        if dataSort["mod16"][i]:
            canalrange_max=canalmax_mod16
            canalrange_min=canalmin_mod16
        else:
            canalrange_max=canalmax_mod32
            canalrange_min=canalmin_mod32
    # on détecte les canaux dépassant le seuil.
    # On décompte le nombre de canaux dépassant le seuil, il doit être compris entre nb_canaux_min et nb_canaux_max pour que ce soit un cas potentiel de charge.
    # On identifie également si le canal avait dépassé le seuil précedemment pour identifier les cas potentiels de bug.
        t=False
        for canal in range(canalrange_min, canalrange_max+1): # enlever les bords
            if dataSort['E'+str(canal)][i]>seuil:
                n+=1
                if liste_canaux[canal-1] and cas_consec>0:
                    t=True
                liste_canaux[canal-1]=True
            else:
                liste_canaux[canal-1]=False

    # bug_consec compte le nombre de fois qu'un même canal dépasse le seuil
        if t:
            bug_consec+=1
        else:
            bug_consec=0

    # cas_consec compte le nombre de fois qu'un bon nombre de canaux dépasse le seuil
        if nb_canaux_min <= n <= nb_canaux_max:
            cas_consec+=1
        else:
            cas_consec=0

    # si bug_consec atteint un nombre critique, on considère qu'il s'agit d'un bug
        if bug_consec==pas_bug:
            cas_consec=0

    # si cas_consec atteint un nombre critique, on considère qu'il s'agit d'un cas de charge
        if cas_consec==nb_pas:
            liste_cas.append([i,dataSort['Center_time'][i]])

        # if i%10==0:
        #     print(str(cas_consec)+'   '+str(n))

    return liste_cas

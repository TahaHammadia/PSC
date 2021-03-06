import pandas as pd
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



def CasdeCharge2(dataSort, args=[500,200,1,3,5,2,22,2,12,2]):
    """
    Renvoie une liste de couples indice-instant des cas de charge identifiés et des infos sur la détection.
    Un cas de charge correspond à une succession suffisament longue de dépassement de seuil de count dans un nombre restreint de canaux, tandis que les autres restent en dessous d'un autre seuil.
    """

    seuil_actif=args[0]
    seuil_inactif=args[1]
    nb_canaux_min=args[2]
    nb_canaux_max=args[3]
    nb_pas=args[4]
    pas_bug=args[5]
    canalmax_mod32=args[6]
    canalmin_mod32=args[7]
    canalmax_mod16=args[8]
    canalmin_mod16=args[9]



    key=['Center_time'] +  ["E" + str(i) for i in range(1, 33)] + ['MLT','INVLAT','mod16']+['cas_consec','bug_consec']
    infos=pd.DataFrame(columns=key)


    liste_cas=[]

    cas_consec=0
    bug_consec=0



    for i in dataSort.index:
    # on parcourt la dataframe triée ligne par ligne

        liste_canal=32*[0]
        n_sup=0
        n_inf=0

    # on identifie le mod (16 ou 32 canaux)
        if dataSort["mod16"][i]:
            canalrange_max=canalmax_mod16
            canalrange_min=canalmin_mod16
        else:
            canalrange_max=canalmax_mod32
            canalrange_min=canalmin_mod32


    # on décompte les canaux dépassant le seuil d'activation et ceux le seuil d'incativation.
    # Ceux du seuil d'activation doivent être plus nombreux que nb_canaux_min, tandis que ceux du seuil d'inactivation doivent être moins nombreux que nb_canaux_min.

        t=False
        for canal in range(canalrange_min, canalrange_max+1): # enlever les bords

            A=dataSort['E'+str(canal)][i]

            if A>seuil_inactif:

                liste_canal[canal-1]=1
                n_inf+=1

                if A>seuil_actif:

                    liste_canal[canal-1]=2
                    n_sup+=1


                    if len(infos)>1 and i-1 in infos.index and infos['E'+str(canal)][i-1]==2:
                        t=True


            # if i%10==0:
            #     print('E'+str(canal)+'  : '+str(A)+'  '+str(A>seuil_inactif)+'   '+str(A>seuil_actif))


    # bug_consec compte le nombre de fois qu'un même canal dépasse le seuil
        if t:
            bug_consec+=1
        else:
            bug_consec=0

    # cas_consec compte le nombre de fois qu'un bon nombre de canaux dépasse le seuil
        if nb_canaux_min <= n_sup and n_inf <= nb_canaux_max:
            cas_consec+=1
        else:
            cas_consec=0

    # si bug_consec atteint un nombre critique, on considère qu'il s'agit d'un bug
        if bug_consec==pas_bug:
            cas_consec=0

    # si cas_consec atteint un nombre critique, on considère qu'il s'agit d'un cas de charge
        if cas_consec==nb_pas:
            liste_cas.append([i,dataSort['Center_time'][i]])

        S=[dataSort['Center_time'][i]]+liste_canal+[dataSort['MLT'][i],dataSort['INVLAT'][i],dataSort['mod16'][i]]+[cas_consec]+[bug_consec]
        infos=infos.append({key[j] : S[j] for j in range(len(S))},ignore_index=True)


        # if i%10==0:
        #     print(str(cas_consec)+'   '+str(n_inf)+'   '+str(n_sup))
    print("liste_cas  :", liste_cas)
    return liste_cas,infos


def CasdeCharge3(dataSort, args=[500,200,1,3,5,2,22,2,12,2]):
    """
    Renvoie une liste de couples indice-instant des cas de charge identifiés et des infos sur la détection.
    Un cas de charge correspond à une succession suffisament longue de dépassement de seuil de count dans un nombre restreint de canaux, tandis que les autres restent en dessous d'un autre seuil.
    Permet de collecter d'une façon optimisée les données relatives aux cas de charges pour une analyse ultérieure.
    Nous allons considérer qu'un cas de charge peut occuper une durée de 10 min (ceci se justifie à partir du rapport AMBRE).
    """

    seuil_actif=args[0]
    seuil_inactif=args[1]
    nb_canaux_min=args[2]
    nb_canaux_max=args[3]
    nb_pas=args[4]
    pas_bug=args[5]
    canalmax_mod32=args[6]
    canalmin_mod32=args[7]
    canalmax_mod16=args[8]
    canalmin_mod16=args[9]



    key=['Center_time'] +  ["E" + str(i) for i in range(1, 33)] + ['MLT','INVLAT','mod16']+['cas_consec','bug_consec']


    liste_cas=[]

    cas_consec=0
    bug_consec=0



    for i in dataSort.index:
    # on parcourt la dataframe triée ligne par ligne

        n_sup=0
        n_inf=0

    # on identifie le mod (16 ou 32 canaux)
        if dataSort["mod16"][i]:
            canalrange_max=canalmax_mod16
            canalrange_min=canalmin_mod16
        else:
            canalrange_max=canalmax_mod32
            canalrange_min=canalmin_mod32


    # on décompte les canaux dépassant le seuil d'activation et ceux le seuil d'incativation.
    # Ceux du seuil d'activation doivent être plus nombreux que nb_canaux_min, tandis que ceux du seuil d'inactivation doivent être moins nombreux que nb_canaux_min.
        second = False
        t=False
        for canal in range(canalrange_min, canalrange_max+1): # enlever les bords

            A=dataSort['E'+str(canal)][i]

            if A>seuil_inactif:

                n_inf+=1

                if A>seuil_actif:

                    n_sup+=1
                    if second:
                        t=True
                    second = True
                else : second = False

            # if i%10==0:
            #     print('E'+str(canal)+'  : '+str(A)+'  '+str(A>seuil_inactif)+'   '+str(A>seuil_actif))


    # bug_consec compte le nombre de fois qu'un même canal dépasse le seuil
        if t:
            bug_consec+=1
        else:
            bug_consec=0

    # cas_consec compte le nombre de fois qu'un bon nombre de canaux dépasse le seuil
        if nb_canaux_min <= n_sup and n_inf <= nb_canaux_max:
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
        #     print(str(cas_consec)+'   '+str(n_inf)+'   '+str(n_sup))
    return liste_cas
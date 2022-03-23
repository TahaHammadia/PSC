import pandas as pd
from sys import path
from main import ad

path.append(ad)

from temps import temps
from data import lire

def charge_ligne(fichier_ions,fichier_e,ligne_debut,ligne_fin):
    """
    Permet de lire les fichiers ASCII des ions et desélectrons entre des bornes qui sont des arguments.
    Génère deux dataframes ions et électrons qu'elle joint. Dans un premier temps, on suppose que les mesures correspondent aux mêmes mesures.
    Le dataframe renvoyé comporte comme colonnes 'key': le temps, les count sur chaque canal d'énergie pour les ions, l'indication du mode pour les ions, les count pour chaque canal d'énergie pour les électrons, l'indication du mode pour les électrons.
    """

    ions_table=lire(fichier_ions,ligne_debut,ligne_fin)
    e_table=lire(fichier_e,ligne_debut,ligne_fin)

    ions=pd.DataFrame(data = ions_table, columns = ['Center_time','Time_range_validity','Center_energy','Energy_range_validity','Product_number','Count'])

    es=pd.DataFrame(data = e_table, columns = ['Center_time','Time_range_validity','Center_energy','Energy_range_validity','Product_number','Count'])



    IE = ["IE" + str(i) for i in range(1, 33)]
    EE = ["EE" + str(i) for i in range(1, 33)]
    key=['Center_time'] +  IE + ['Imod16'] + EE + ['Emod16'] + ["potentiel"]

    datS=[]


    SI=[]
    SE = []

    for i in ions.index:
    #   On passe d'une dataframe qui a une entrée par instant-énergie à une dataframe qui a une entrée par instant
    #   ions possède une périodicité de 32 vis-à-vis des énergies, vu qu'il y a 32 canaux
    #   on accumule donc les count dans une liste qu'on décharge une fois toute les 32 lignes
    #   les count correspondent donc aux énergies de leur indice modulo 32 (si le fichier commence bien au premier canal)
        if i%32==17:
            mod16_IE = abs(float(ions['Center_energy'][i])) < 1
            mod16_EE = abs(float(es['Center_energy'][i])) < 1
    #         on vérifie si on est en mode de détection 16 ou 32 canaux en testant si l'energie du 17eme canal est 0


        if i%32==0 and i!=0:

            t = temps(ions['Center_time'][i-1])

            S=[t]+SI+[mod16_IE]+SE+[mod16_EE]+[0]

            datS.append(S)
            S = []
            SI = []
            SE = []


        SI.append(ions['Count'][i])
        SE.append(es['Count'][i])

    dat=pd.DataFrame(data=datS, columns=key)

    del ions_table
    del e_table
    del datS

    return dat
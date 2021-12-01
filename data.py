"""
Les fonctions de ce fichier permettent de passer d'un fichier ASCII généré par CLweb à une représentation pandas.
"""



from astropy.io import ascii
import pandas as pd
from sys import path
from linecache import getline, checkcache, clearcache
from numpy import array, transpose

ad_may="A:/Travail/X/PSC/python/"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

#ad=ad_may
ad=ad_taha

path.append(ad)

from temps import temps


def traiter(datum):
    """
    Cette fonction traite la liste qu'on obtient en extractant une ligne d'un fichier ASCII de CLweb. Elle permet entre autres d'éliminer les espaces et le caractère Z inutiles. Elle renvoie une liste propre des données, ordonnées selon les colonnes de notre dataframe.
    """

    x = []
    for i in range(len(datum)):
        datum[i] = datum[i].lstrip()
        if datum[i]!='':
            if datum[i][-2]!='Z':
                datum[i]=float(datum[i][:-1])
            x.append(datum[i])


    return x


def lire(fichier, ligne_debut, ligne_fin):
    """
    Permet de lire un fichier entre une ligne de début et une ligne de fin.
    Renvoie une liste de liste de données, comme une matrice. Celle-ci sera ensuite transformée en dataframe.
    """

# Comme d'hab, ligne_debut incluse, ligne_fin exclue. Le compte des lignes commence de 1 (pas comme d'hab).
    res = []
    for i in range(ligne_debut, ligne_fin + 1):
        datum = getline(fichier, i).split(" ")
        datum = traiter(datum)
        res.append(datum)
    # checkcache(fichier)
    clearcache()
    return res



def charge_ligne(fichier_ions,fichier_mlt,ligne_ions_debut,ligne_ions_fin,ligne_mlt_debut,ligne_mlt_fin):
    """
    Permet de lire les fichiers ASCII des ions et de position (MLT et INVLAT) entre des bornes qui sont des arguments.
    Génère deux dataframes ions et mlt qu'elle joint avec la condition de temps.
    Le dataframe renvoyé comporte comme colonnes 'key': le temps, les count sur chaque canal d'énergie, le mlt, l'invlat et si le mode courant est 16 canaux ou 32.
    Renvoie également l'indice de fin du parcours du fichier_mlt.
    """

    ions_table=lire(fichier_ions,ligne_ions_debut,ligne_ions_fin)
    mlt_table=lire(fichier_mlt,ligne_mlt_debut,ligne_mlt_fin)

    ions=pd.DataFrame(data = ions_table, columns = ['Center_time','Time_range_validity','Center_energy','Energy_range_validity','Product_number','Count'])

    mlt=pd.DataFrame(data = mlt_table, columns =['Center_time','MLT','INVLAT'])


    E = ["E" + str(i) for i in range(1, 33)]
    key=['Center_time'] +  E + ['MLT','INVLAT','mod16']

    dat=pd.DataFrame(columns=key)


    S=[]
    k=0
    l=len(mlt)
    seuil_temp = 3
    bool_pos = True

    for i in ions.index:
    #   On passe d'une dataframe qui a une entrée par instant-énergie à une dataframe qui a une entrée par instant
    #   ions possède une périodicité de 32 vis-à-vis des énergies, vu qu'il y a 32 canaux
    #   on accumule donc les count dans une liste qu'on décharge une fois toute les 32 lignes
    #   les count correspondent donc aux énergies de leur indice modulo 32 (si le fichier commence bien au premier canal)
        if i%32==17:
            mod16 = abs(float(ions['Center_energy'][i])) < 1
    #         on vérifie si on est en mode de détection 16 ou 32 canaux en testant si l'energie du 17eme canal est 0


        if i%32==0 and i!=0:

            t = temps(ions['Center_time'][i-1])

            while abs(t.duration(temps(mlt['Center_time'][k]))) >= seuil_temp  and k<l:
                if t.duration(temps(mlt['Center_time'][k])) < 0 :
                    bool_pos = False
                    break
                k+=1

                # On descend la liste et on prend le premier instant tel que : |t' - t| < 1 s.
                # Sinon, on met 0,0 ; la ligne sera refusée par le tri.

            if bool_pos :
                S=[t]+S+[mlt['MLT'][k],mlt['INVLAT'][k],mod16]
            else :
                S=[t]+S+[0,0,mod16]

            dat=dat.append({key[j] : S[j] for j in range(len(S))},ignore_index=True)
            S = []


        S.append(ions['Count'][i])

    del ions_table
    del mlt_table
    del mlt

    return dat,k
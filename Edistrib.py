
from dataElec import charge_ligne
from tracking_potentiel import tracking
from distribution import distrib_corr
import pandas as pd
from math import sqrt

from main import ad

import optMax


def distrib(dossier, args, ligne_debut=1, ligne_fin=2720, coupure=3):
    """
    dossier: adresse des fichiers des données des ions et éléctrons
    args: paramètres de CasdeCharge2 utilisés ici par tracking
    ligne_debut: ligne de début des données chargées des fichiers ions et électrons
    ligne_fin: ligne de fin
    coupure: nombre de premiers canaux retirés de la dataframe car n'ayant pas la même correction (électrons réémis)

    Construit une dataframe dist des valeurs corrigées ncorr et Ereel de la fonction de distribution par énergie des électrons à chaque instant à partir des données entre les lignes sélectionnées. Contient également le potentiel.
    Les colonnes de dist sont donc:
    'Center_time': instant de mesure de la classe temps
    'n': liste des valeurs de la fonction de distribution par énergie des électrons en m^-3 eV^-1
    'E': liste des énergies correspondantes en eV
    'mod16': booléen du mode de mesure 16 ou 32 canaux
    'U': potentiel du satellite
    """

    fichier_ions=ad+"data/"+dossier+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
    fichier_e=ad+"data/"+dossier+"/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"

    dat=charge_ligne(fichier_ions,fichier_e,ligne_debut,ligne_fin)

    tracking(dat,args)

    S=[]

    for L in dat.values:
        mod16=L[-2]
        ncorr,Ereel= distrib_corr(L[34:66],L[67],L[66])
        S.append([L[0],ncorr[coupure:],Ereel[coupure:],mod16,L[67]])

    dist=pd.DataFrame(data=S, columns=['Center_time','n','E','mod16','U'])

    return dist


def moyenne_temporelle(dist,index_debut=1,index_fin=-1):
    """
    dist: dataframe de distribution construite par distrib
    index_debut: index de début de la moyenne
    index_fin: index de fin, par défaut la longueur de la distribution

    Construit les listes n et E aggrégeant toutes les données de distribution entre les index choisis. Ainsi que la moyenne du potentiel U et son écart type s.
    """

    if index_fin<0:
        index_fin=len(dist)

    n=[]
    E=[]
    U=0
    VU=0

    for i in range(index_debut,index_fin):

        if dist['U'][i]!=None and not (pd.isna(dist['U'][i])):

            n+=(dist['n'][i])
            E+=(dist['E'][i])
            U+=dist['U'][i]
            VU+=dist['U'][i]**2

    if index_fin>index_debut:
        U/=(index_fin-index_debut)
        VU/=(index_fin-index_debut)
        s=sqrt(VU-U**2)

    return n,E,U,s


def MXWdist(dist, n_max, seuil = None, inf = True, modSeuil = False):
    """
    dist: dataframe de distribution construite par distrib
    n_max: nombre de maxwelliennes
    seuil, inf, modSeuil: paramètres de optdist

    Construit une dataframe distMXW contenant toutes les données de dist plus les paramètres des maxwelliennes optimales à chaque instant ainsi que leurs valeurs n_mxw aux énergies E.
    Ainsi distMXW possède les informations des maxweliennes à chaque instant prêtes à être réutilisées, et les valeurs n_mxw permettent de tracer les courbes sans avoir à recalculer.
    Les colonnes des distMXW sont:
    'Center_time': instant de mesure de la classe temps
    'mod16': booléen du mode de mesure 16 ou 32 canaux
    'MXW_parameters': paramètres des maxweliennes sous forme de liste
    'MXW_covar': covariance des maxweliennes par rapport aux données
    'n_mxw': liste des valeurs de la fonction de distribution calculées avec les maxweliennes
    'n': liste des valeurs de la fonction de distribution par énergie des électrons en m^-3 eV^-1
    'E': liste des énergies correspondantes en eV
    'U': potentiel du satellite
    """

    S=[]

    for i in range (len(dist)):

        try:
            best_vals,covar=optdist(dist, i, n_max, seuil, inf, modSeuil)
            S.append([dist['Center_time'][i],dist['mod16'][i],best_vals,covar,[fmxw(E,best_vals) for E in dist['E'][i]],dist['n'][i],dist['E'][i],dist['U'][i]])

        except ValueError:
            continue

        except KeyboardInterrupt:
            continue

        except RuntimeError:
            continue


    distMXW=pd.DataFrame(data=S, columns=['Center_time','mod16','MXW_parameters','MXW_covar','n_mxw','n','E','U'])

    return distMXW

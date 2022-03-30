
from dataElec import charge_ligne
from tracking_potentiel import tracking
from distribution import distrib_corr
import pandas as pd
from math import sqrt

from main import ad

import optMax


def distrib(dossier, args, ligne_debut=1, ligne_fin=2720, coupure=3):

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

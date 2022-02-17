from scipy.stats import maxwell
import numpy as np
from math import pow
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sys import path

ad_may="A:/Travail/X/PSC/python/"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

#ad=ad_may
ad=ad_taha

path.append(ad)

from dataElec import charge_ligne
from tracking_potentiel import tracking
from distribution import distrib_corr

fichier_ions = "C:/Users/hp 650 G3/Desktop/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
fichier_e = "C:/Users/hp 650 G3/Desktop/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"
args = [680, 50, 1, 4, 3, 2, 26, 2, 14, 2, 15]
ligne = 38


# Fonctions de base
me=9.11e-31 ## e- mass [kg]
qe=1.6e-19  ## e- chage [C]
kB = 1.380e-23  ## Boltzman constant [IS]

def maxE(E, n, T):
    """
    Ici, T est la température équivalente en eV
    """
    try:
        return 2/np.sqrt(np.pi) * n * np.sqrt(E*qe) / pow(abs(T)*qe, 1.5) * np.exp(-E/T)  # on multiplie par qe pour convertir en SI
    except:
        print(E, n, T)
        raise(KeyboardInterrupt)

def fct2maxwell(E, n1, T1, n2, T2):
    return maxE(E, n1, T1) + maxE(E, n2, T2)


# Optimisation
def optimise(seuil, inf = True):
    """
    Permet d'optimiser les paramètres de la distribution à deux maxwelliennes
    """
    dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)
    tracking(dat, args)
    liste_count_electr = [dat["EE" + str(k)][ligne] for k in range(1, 33)]
    potentiel = dat["potentiel"][ligne]
    mod16 = dat["Emod16"][ligne]
    ncorr,Ereel = distrib_corr(liste_count_electr,potentiel,mod16)
    idx=0

    if inf:
        for i in range(len(Ereel)):
            if Ereel[i] + potentiel > seuil:
                idx = i
                break
        idx1 = (len(ncorr)-idx)//3
        idx2 = 2*idx1
        idx1+= idx
        idx2+=idx
        best_vals, covar = curve_fit(fct2maxwell, Ereel[idx:], ncorr[idx:], p0 = [ncorr[idx1], Ereel[idx1], ncorr[idx2], Ereel[idx2]])

    else:
        for i in range(len(Ereel)):
            if Ereel[i] + potentiel > seuil:
                idx = i
                break
        idx1 = idx//3
        idx2 = 2*idx1
        best_vals, covar = curve_fit(fct2maxwell, Ereel[:idx+1], ncorr[:idx+1], p0 = [ncorr[idx1], Ereel[idx1], ncorr[idx2], Ereel[idx2]])

    print('best_vals: {}'.format(best_vals))
    print('covar: {}'.format(np.sqrt(np.diag(covar))))
    return best_vals
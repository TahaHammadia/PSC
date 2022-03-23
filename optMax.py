from scipy.stats import maxwell
import numpy as np
from math import pow
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


# Fonctions de base
me=9.11e-31 ## e- mass [kg]
qe=1.6e-19  ## e- chage [C]
kB = 1.380e-23  ## Boltzman constant [IS]

def maxE(E, n, T):
    """
    Ici, T est la température équivalente en eV
    """
    try:
        return 2/np.sqrt(np.pi) * n * qe * np.sqrt(E*qe) / pow(abs(T)*qe, 1.5) * np.exp(-E/T)  # on multiplie par qe pour convertir en SI
    except:
        print(E, n, T)
        raise(KeyboardInterrupt)

def fct2maxwell(E, n1, T1, n2, T2):
    return maxE(E, n1, T1) + maxE(E, n2, T2)

def fct3maxwell(E, n1, T1, n2, T2, n3, T3):
    return maxE(E, n1, T1) + maxE(E, n2, T2) + maxE(E, n3, T3)

fcts_max = [maxE, fct2maxwell, fct3maxwell]


# Fonction d'optimisation avec tracking
def optimise(dat, ligne, args, n_max, seuil = None, inf = True, modSeuil = False):
    """
    Permet d'optimiser les paramètres de la distribution à deux maxwelliennes

    dat : dataframe du fichier à analyser
    ligne : ligne à traiter dans le pandas.dataframe (la ligne est prise modulo la taille
    args : arguments utilisés dans notre détection de cas

    n_max : nombre de maxwelliennes utilisées pour le fitting
    inf : déclare si on élimine la partie inférieure ou supérieur du spectre
    seuil : seuil qui délimite les potentiels sur lesquels on optimise
    """

    if ligne >= dat.size:
        raise(ValueError("Ligne demandée inexistante"))

    tracking(dat, args)
    liste_count_electr = [dat["EE" + str(k)][ligne] for k in range(1, 33)]
    potentiel = dat["potentiel"][ligne]
    if potentiel != potentiel : raise(ValueError)
    mod16 = dat["Emod16"][ligne]
    ncorr,Ereel = distrib_corr(liste_count_electr,potentiel,mod16)
    idx=0

    # Séparation selon le seuil et valeur initiales de l'optimisation

    if modSeuil:
        seuil_test = seuil - potentiel
    else:
        seuil_test = potentiel * 0.2
    for i in range(len(Ereel)):
        if Ereel[i] > seuil_test :
            idx = i
            break

    if inf:
        idX = [idx + k * (len(ncorr) - idx) // (n_max + 1) for k in range(1, 1 + n_max)]
    else:
        idX = [k * idx // (n_max + 1) for k in range(1, 1 + n_max)]

    # Optimisation
    P0 = []
    for i in range(n_max):
        P0.append(ncorr[idX[i]])
        P0.append(Ereel[idX[i]])
    best_vals, covar = curve_fit(fcts_max[n_max - 1], Ereel[idx:], ncorr[idx:], p0 = P0, check_finite = True)

    print('ligne:{}'.format(ligne))
    print('best_vals: {}'.format(best_vals))
    print('covar: {}'.format(np.sqrt(np.diag(covar))))
    return best_vals, covar, ncorr, Ereel
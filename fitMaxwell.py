from scipy.stats import maxwell
import numpy as np
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


# Fonctions de base
def P(x, a):
    return np.sqrt(2/np.pi)* (x**2*np.exp(-x**2/(2*a**2)))/a**3

def fct3maxwell(x, m1, s1, m2, s2, m3, s3, a):
    y1 = P(x-m1, s1)
    y2 = P(x-m2, s2)
    y3 = P(x-m3, s3)
    return a*(y1 + y2 + y3)



# Fonctions intermédiaires pour le fit
def maxFit(ncorr, Ereel):
    """
    Retourne un fit avec une seule maxwellienne.
    Simule une base de données à partir des valeurs des densités corrigées.
    Retourne les nombres utilisés.
    """
    n = len(Ereel)

    data = []
    N = []
    for i in range(n):
        N.append(int(ncorr[i] + .5))  # avoir bcp de valeurs permet d'avoir un fit plus précis
        data = data + [Ereel[i]] * N[i]
    return maxwell.fit(data)


def maxFitFile(ncorr,Ereel, mod16):
    if mod16:
        idx1, idx2 = 5, 10
    else:
        idx1, idx2  = 11, 22
    m1, s1 = maxFit(ncorr[:idx1], Ereel[:idx1])
    m2, s2 = maxFit(ncorr[idx1:idx2], Ereel[idx1:idx2])
    m3, s3 = maxFit(ncorr[idx2:], Ereel[idx2:])
    return [m1, s1, m2, s2, m3, s3]



def fit_max_par(fichier_ions, fichier_e, ligne, args, a, ncorr,Ereel, mod16):
    """
    a est un facteur multiplicatif qu'on doit déterminer
    """
    init_vals = np.array(maxFitFile(ncorr,Ereel, mod16) + [a])
    best_vals, covar = curve_fit(fct3maxwell, Ereel, ncorr, p0=init_vals)
    return np.sqrt(np.diag(pcov))



# Fonction principale
def fit_max(fichier_ions, fichier_e, ligne, args):
    """
    Permet de déterminer les variables en optimisant le facteur multiplicatif a en minimisant l'écart-type.
    """
    dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)
    tracking(dat, args)
    liste_count_electr = [dat["EE" + str(k)][ligne] for k in range(1, 33)]
    potentiel = dat["potentiel"][ligne]
    mod16 = dat["Emod16"][ligne]
    ncorr,Ereel = distrib_corr(liste_count_electr,potentiel,mod16)



    A = np.linspace(1, 10000, num = 100) # à trouver !!
    loss = float('inf')
    a_res = None
    for a in A:
        try:
            if fit_max_par(fichier_ions, fichier_e, ligne, args, a, ncorr,Ereel,mod16) < loss:
                a_res = a
        except:
            continue
    if not (a_res is None):
        init_vals = np.array(maxFitFile(ncorr,Ereel, mod16) + [a_res])
        best_vals, covar = curve_fit(fct3maxwell, Ereel, ncorr, p0=init_vals)
        print('best_vals: {}'.format(best_vals))
    else:
        print("Échec")

#[559.2301741237069, 21.39477382989631, 370.6739453645084, 373.6288048243284, -2069.8630727315517, 4762.318472841551, 9799/0.01]
#print('best_vals: {}'.format(best_vals))
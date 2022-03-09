from sys import path
import matplotlib.pyplot as plt

ad_may="A:/Travail/X/PSC/python/"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

#ad=ad_may
ad=ad_taha

path.append(ad)
from optMax import *

fichier_ions = "C:/Users/hp 650 G3/Desktop/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
fichier_e = "C:/Users/hp 650 G3/Desktop/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"
args = [680, 50, 1, 4, 3, 2, 26, 2, 14, 2, 15]


ligne = 38
n_max = 2
Seuil = 500

dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)
for ligne in range(len(dat.index)):
    try:
        best_vals, ncorr, Ereel = optimise(dat, ligne, args, n_max, seuil = Seuil, modSeuil = True)
    except ValueError:
        continue
    except RuntimeError:
        continue

    plt.scatter(Ereel, ncorr)

    if n_max == 1:
        val = [fcts_max[0](E, best_vals[0], best_vals[1]) for E in Ereel]
    if n_max == 2:
        val = [fcts_max[1](E, best_vals[0], best_vals[1], best_vals[2], best_vals[3]) for E in Ereel]
    if n_max == 3:
        val = [fcts_max[2](E, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4], best_vals[5]) for E in Ereel]

    plt.plot(Ereel, val)

    plt.xscale("log")
    plt.yscale("log")
    plt.show()
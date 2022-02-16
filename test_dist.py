import numpy as np
import matplotlib.pyplot as plt

fichier_ions = "C:/Users/hp 650 G3/Desktop/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
fichier_e = "C:/Users/hp 650 G3/Desktop/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"
dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)


args = [680, 50, 1, 4, 3, 2, 26, 2, 14, 2, 15]

tracking(dat, args)

liste_count_electr = [dat["EE" + str(k)][14] for k in range(1, 33)]

potentiel = dat["potentiel"][14]

mod16 = dat["Emod16"][14]

ncorr,Ereel = distrib_corr(liste_count_electr,potentiel,mod16)

x, N = maxFit(ncorr[10:], Ereel[10:])

N = [elt / max(N) * 0.01 for elt in N]

plt.scatter(Ereel[10:], N)

dist = maxwell(loc = x[0], scale = x[1])
X = np.linspace(Ereel[0], 30000, 10000)
plt.plot(X, dist.pdf(X))


plt.xscale('log')
plt.yscale('log')

plt.show()
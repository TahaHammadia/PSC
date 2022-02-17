dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)
tracking(dat, args)
liste_count_electr = [dat["EE" + str(k)][ligne] for k in range(1, 33)]
potentiel = dat["potentiel"][ligne]
mod16 = dat["Emod16"][ligne]
ncorr,Ereel = distrib_corr(liste_count_electr,potentiel,mod16)

plt.scatter(Ereel, ncorr)

x=optimise(500)
y = optimise(100, False)
val1 = [fct2maxwell(E, x[0], x[1], x[2], x[3]) for E in Ereel]
plt.plot(Ereel, val1)

val2 = [fct2maxwell(E, y[0], y[1], y[2], y[3]) for E in Ereel]
plt.plot(Ereel, val2)

plt.xscale("log")
plt.yscale("log")
plt.show()
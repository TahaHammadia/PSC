for i in dat.index:

    liste_count_electr = [dat["EE" + str(k)][i] for k in range(1,33)]
    potentiel = dat["potentiel"][i]
    mod16 = dat['Emod16'][i]

    print(distrib_corr(liste_count_electr,potentiel,mod16), potentiel)

    input("")
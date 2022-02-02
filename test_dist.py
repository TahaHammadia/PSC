fichier_ions = "C:/Users/hp 650 G3/Desktop/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
fichier_e = "C:/Users/hp 650 G3/Desktop/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"
dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)


args = [680, 50, 1, 4, 3, 2, 26, 2, 14, 2, 15]

energies = tracking(dat, args)
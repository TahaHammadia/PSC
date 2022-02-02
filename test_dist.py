fichier_ions = "C:/Users/hp 650 G3/Desktop/obj3_Panel01_JASON3_AMBRE_P09_SC1.asc"
fichier_e = "C:/Users/hp 650 G3/Desktop/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
dat = charge_ligne(fichier_ions, fichier_e, 1, 1760)


args = [0]*10

args[0] = 50

args[6] = 32

args[7] = 1

args[8] = 16

args[9] = 1

tracking(dat, args)
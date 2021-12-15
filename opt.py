from sys import path

path.append("C:/Users/hp 650 G3/Documents/GitHub/PSC")
from main import Analyse2Test

setSeuilActif = [i for i in range(100, 1010, 10)] # seuil_actif
setSeuilInactif = [j for j in range(50, 1000, 10)]# seuil inactif
#setCanaux = [(i,j) for i in range(2, 4) for j in range(1, i)] # nb_canaux_max, nb_canaux_min
setPas = [i for i in range(3, 10)] # nb_pas
setBug = [j for j in range(2, 9)]  #pas_bug
#setMod32 = [(i,j) for i in range(24, 33) for j in range(1, min(i, 8))] # canalmax_mod32, canalmin_mod32
#setMod16 = [(i,j) for i in range(12, 17) for j in range(1, min(i, 4))] # canalmax_mod16, canalmin_mod16
setVide = [i for i in range(7, 16)] # nbr_vide

pasid = []

ud0 = "C:/Users/hp 650 G3/Documents/GitHub/PSC/File[0]/"
ud1 = "C:/Users/hp 650 G3/Documents/GitHub/PSC/File[1]/"

f_ions = "obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
f_mlt = "obj7.asc"
f_idx = "indice.txt"
f_res = "resultat.txt"


files0 = list([tuple(ud0 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["16_04_2017_16.56/", "16_07_2017_01.13/", "16_07_2017_19.29/", "17_09_2019_08.57/", "02_05_2016_15.06/", "28_03_2016_19.07/", "05_04_2016_16.22/", "05_04_2016_18.16/", "27_04_2016_13.14/", "01_05_2016_20.22/", "03_01_2020_07.19/", "05_01_2020_00.30/", "25_03_2020_11.38/", "25_06_2020_18.24/", "25_06_2020_18.26/", "27_06_2018_20.14/"]])

files1 = list([tuple(ud1 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["20_10_2017_02.41/", "28_01_2018_01.06/", "28_05_2017_4.38/", "31_10_2019_00.02/", "01_01_2017_05.14/", "13_06_2018_22.41/", "13_06_2018_22.51/", "27_09_2019_01.09/", "03_06_2017/", "07_03_2017/", "09_04_2017/", "09_12_2017/", "14_10_2017/", "19_05_2017/", "21_03_2017/", "21_04_2017/", "21_11_2017/", "25_10_2017/", "28_05_2017/"]])

files = [files0, files1]

def init():
    for file in files0 + files1:
        Nions = sum(1 for line in open(file[0]))
        Nmlt = sum(1 for line in open(file[1]))
        with open(file[2], 'w') as f:
            f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])


def loss(idx, files):
    """
    files est un tuple ou liste dont le premier élément est une liste de cas de charges et le second une liste de non cas de charges.
    """
    try :

        return lossDict[idx][0]

    except KeyError:
        N = (len(files[0]) + len(files[1])) / 2
        cpt = [0, 0]

        for i in range(2):
            for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in files[i] :

                args = [set[idx][0], set[idx][1], default[0], default[1], set[idx][2], set[idx][3], default[2], default[3], default[4], default[5], set[idx][4]]

                cal = Analyse2Test(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args)
                infoDict[idx] = cal[0]
                if cal[1]: cpt[i] += 1

        if cpt[0] == 0: val = float('inf')

        else: val = (len(files[0]) - cpt[0] + alpha * cpt[1]) / N

        lossDict[idx] = val, (len(files[0]) - cpt[0]) / N, cpt[1] / N
        return val

def opt_int(idx, lossValue = float('inf'), pas = 800):
    """
    À modifier...
    """
    idx0, lossValue0, pas0 = idx, lossValue, pas
    try:
        res = idxDict[(idx0, lossValue0, pas0)]
    except KeyError:
        for file in files[0] + files[1]:
            with open (file[2]) as f:
                iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))
            with open(file[2], 'w') as f:
                f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])

        while pas >= 1:
            idx, pas, lossValue = next(idx, pas, lossValue)
        idxDict[(idx0, lossValue0, pas0)] = idx, lossValue, pas
        res = idx, lossValue, pas
    with open("C:/Users/hp 650 G3/Documents/GitHub/PSC/res.txt", 'a') as f:
        f.write(str(idx0) + ' ' + str(lossValue0) + ' ' + str(pas0) + ' :: ' + str(idx) + ' ' + str(lossValue) + ' ' + str(pas) + str(lossDict[idx][1]) + " " + str(lossDict[idx][2]) + '\n')
    return res

#init()
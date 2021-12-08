from sys import path

path.append("C:/Users/hp 650 G3/Documents/GitHub/PSC")
from main import Analyse2Test

setSeuil = [(i,j) for i in range(100, 1010, 10) for j in range(50, i, 10)] # seuil_actif, seuil_inactif
#setCanaux = [(i,j) for i in range(2, 4) for j in range(1, i)] # nb_canaux_max, nb_canaux_min
setPas = [(i,j) for i in range(3, 10) for j in range(2, i)] # nb_pas, pas_bug
#setMod32 = [(i,j) for i in range(24, 33) for j in range(1, min(i, 8))] # canalmax_mod32, canalmin_mod32
#setMod16 = [(i,j) for i in range(12, 17) for j in range(1, min(i, 4))] # canalmax_mod16, canalmin_mod16
setVide = [i for i in range(7, 16)] # nbr_vide

set = [(a, b, c, d,e) for a,b in setSeuil for c, d in setPas for e in setVide]
N = len(set)
idx = N // 2
#573306

default = 1, 3, 26, 2, 14, 2

pas = 100 * 4 * 2

alpha = 0.3

lossValue = float('inf')

ud0 = "C:/Users/hp 650 G3/Desktop/Test/File[0]/"
ud1 = "C:/Users/hp 650 G3/Desktop/Test/File[1]/"

f_ions = "obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
f_mlt = "obj7.asc"
f_idx = "indice.txt"
f_res = "resultat.txt"

files0 = list([tuple(ud0 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["16_04_2017_16.56/", "16_07_2017_01.13/", "16_07_2017_19.29/", "17_09_2019_08.57/", "02_05_2016_15.06/", "28_03_2016_19.07/"]])

files1 = list([tuple(ud1 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["20_10_2017_02.41/", "28_01_2018_01.06/", "28_05_2017_4.38/", "31_10_2019_00.02/"]])

files = [files0, files1]

lossDict = {}
infoDict = {}

def loss(idx, files):
    """
    files est un tuple ou liste dont le premier élément est une liste de cas de charges et le second une liste de non cas de charges.
    """
    N = (len(files[0]) + len(files[1])) / 2
    try :

        return lossDict[idx]

    except KeyError:

        cpt = [0, 0]

        for i in range(2):
            for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in files[i] :

                args = [set[idx][0], set[idx][1], default[0], default[1], set[idx][2], set[idx][3], default[2], default[3], default[4], default[5], set[idx][4]]

                cal = Analyse2Test(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args)
                infoDict[idx] = cal[0]
                if cal[1]: cpt[i] += 1

        if cpt[0] == 0: val = float('inf')

        else: val = (len(files[0]) - cpt[0] + alpha * cpt[1]) / N

        lossDict[idx] = val
        return val


def next(idx, pas, lossValue):
    """
    Calcule et renvoie les prochaines valeurs de idx, pas et lossValue.
    """

    listLoss = [(idx, loss(idx, files))]
    if idx >= pas:
        listLoss.append((idx - pas, loss(idx - pas, files)))
    else:
        listLoss = [(0, loss(0, files))]

    if idx < N - pas:
        listLoss.append((idx + pas, loss(idx + pas, files)))
    else:
        listLoss = [(N - 1, loss(N - 1, files))]

    res = -1
    for i in range(1, 3):
        if listLoss[i][1] < lossValue:
            lossValue = listLoss[i][1]
            res = listLoss[i][0]
    if listLoss[0][1] <= lossValue:
        lossValue = listLoss[0][1]
        res = idx

    if res == -1:
        raise ValueError("lossValue too small")
    if res == idx:
        pas //= 2
    return res, pas, lossValue

for file in files[0] + files[1]:
    with open (file[2]) as f:
        iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))
    with open(file[2], 'w') as f:
        f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])

while pas >= 1:
    idx, pas, lossValue = next(idx, pas, lossValue)


print(idx, pas, lossValue)


# args = [seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide]
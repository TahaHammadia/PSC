setSeuil = [(i,j) for i in range(100, 1010, 10) for j in range(50, i, 10)] # seuil_actif, seuil_inactif
#setCanaux = [(i,j) for i in range(2, 4) for j in range(1, i)] # nb_canaux_max, nb_canaux_min
setPas = [(i,j) for i in range(3, 10) for j in range(2, i)] # nb_pas, pas_bug
#setMod32 = [(i,j) for i in range(24, 33) for j in range(1, min(i, 8))] # canalmax_mod32, canalmin_mod32
#setMod16 = [(i,j) for i in range(12, 17) for j in range(1, min(i, 4))] # canalmax_mod16, canalmin_mod16
setVide = [i for i in range(7, 16)] # nbr_vide

set = [(a, b, c, d,e) for a,b in setSeuil for c, d in setPas for e in setVide]
N = len(set)
idx = N // 2

default = 1, 3, 26, 2, 14, 2

pas = 100 * 4 * 2

lossValue = float('inf')


files = [[],[]

lossDict = {}

def loss(idx, files):
    """
    files est un tuple ou liste dont le premier élément est une liste de cas de charges et le second une liste de non cas de charges.
    """
    try :

        return lossDict[idx_args]

    except KeyError:

        cpt = [0, 0]
        for i in range(2):
            for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in files[i] :
                args = [set[idx][0], set[idx][1], default[0], default[1], set[idx][2], set[idx][3], default[2], default[3], default[4], default[5], set[idx][4]]
                if Analyse2(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args) > 0: cpt[i] += 1
        val = len(files[0]) - cpt[0] + 0.5 * (cpt[1] / cpt[0])
        lossDict[idx_args] = val
        return val

defext(idx, pas, lossValue) n:
    listLoss = [(idx, loss(idx, files))]
    if idx >= pas:
        listLoss.append((idx - pas, loss(idx - pas, files)))
    else:
        listLoss = [(0, loss(0, files))]

    if idx < n - pas:
        listLoss.append((idx + pas, loss(idx + pas, files)))
    else:
        listLoss = [(N - 1, loss(N - 1, files))]
        res = -1
    for i in range(3):
        if listLoss[i][1] < lossValue:
            lossValue = listLoss[i][1]
            res = listLoss[i][0]
    if res == -1:
        raise ValueError("lossValue too small")
        if res == idx:
            pas //= 2
    return res, pas, lossValue

while pas >= 1:
    idx, pas, lossValue = next(idx, pas, lossValue)

print(idx, pas, lossValue)


# args = [seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide]
setMod32 = [(i,j) for i in range(2, 33) for j in range(1, i)] # fixé
setMod16 = [(i,j) for i in range(2, 17) for j in range(1, i)] # fixé
setCanaux = [(i,j) for i in range(2, 5) for j in range(1, i)]
setPas = [(i,j) for i in range(3, 10) for j in range(2, i)]
setSeuil = [(i,j) for i in range(100, 1010, 10) for j in range(50, i, 10)]
setVide = [i for i in range(1, 16)]

files = [,] # à remplir

def loss(args, files):
    """
    On s'arrange pour n'appeler Analyse qu'une fois par fichier.
    files est un tuple ou liste dont le premier élément est une liste de cas de charges et le second une liste de non cas de charges.
    """
    cpt = [0, 0]
    for i in range(2):
        for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in setFilesTrue :
            if Analyse2(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args): cpt[i] += 1
    return len(files[0]) - cpt[0] + 0.5 * (cpt[1] / cpt[0])

lossValue = float('inf')
listMin = []

for canalmax_mod32, canalmin_mod32 in setMod32:
    for canalmax_mod16, canalmin_mod16 in setMod16:
        for nb_canaux_max, nb_canaux_min in setCanaux:
            for nb_pas, pas_bug in setPas:
                for seuil_actif, seuil_inactif in setSeuil:
                    for nbr_vide in SetVide:
                        val = loss([seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide], files)
                        if val < lossValue:
                            loss Value = val
                            listMin = [[seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide]]
                        elif val == lossValue:
                            listMin.append([seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide])

print(lossValue)
print(listMin)
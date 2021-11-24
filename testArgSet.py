setSeuil = [(i,j) for i in range(100, 1010, 10) for j in range(50, i, 10)] # seuil_actif, seuil_inactif
setCanaux = [(i,j) for i in range(2, 4) for j in range(1, i)] # nb_canaux_max, nb_canaux_min
setPas = [(i,j) for i in range(3, 10) for j in range(2, i)] # nb_pas, pas_bug
setMod32 = [(i,j) for i in range(2, 33) for j in range(1, i)] # canalmax_mod32, canalmin_mod32
setMod16 = [(i,j) for i in range(2, 17) for j in range(1, i)] # canalmax_mod16, canalmin_mod16
setVide = [i for i in range(7, 16)] # nbr_vide

files = [,] # à remplir

def loss(args, files):
    """
    files est un tuple ou liste dont le premier élément est une liste de cas de charges et le second une liste de non cas de charges.
    """
    cpt = [0, 0]
    for i in range(2):
        for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in setFilesTrue :
            if Analyse2(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args): cpt[i] += 1
    return len(files[0]) - cpt[0] + 0.5 * (cpt[1] / cpt[0])

lossValue = float('inf')
listMin = []

def next(args, lossValue):
    """
    Fonction qui calcule le prochain argument à tester dans une approche de descente du gradient.
    """

    return nextArg, val


print(lossValue)
print(listMin)

# args = [seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide]
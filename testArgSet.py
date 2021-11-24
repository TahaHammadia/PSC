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

setMod32 = [i,j for i in range(2, 33) for j in range(1, i)]
setMod16 = [i,j for i in range(2, 17) for j in range(1, i)]
setCanaux = [i, j for i in range(2, ) for j in range(1, i)]
setPas = [i, j for i in range(3, 10) for j in range(2, i)]
setSeuil = [i, j for i in range(100, 1010, 10) for j in range(50, i, 10)]
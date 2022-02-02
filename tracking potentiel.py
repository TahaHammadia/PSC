def tracking(database_ions_electrons, args):

    db=database_ions_electrons

    seuil=args[0]
    canalmax_mod32=args[6]
    canalmin_mod32=args[7]
    canalmax_mod16=args[8]
    canalmin_mod16=args[9]

    Energy16=[ 12.65,   20.88,      34.46,    56.89,   93.90,     154.99,    255.85,   422.32,   697.10,   1150.69,   1899.40,   3135.27,  5175.28,  8542.65,  14101.05,  23276.10] #Ce sont les énergies des canaux, on les a dans les fichiers ascii

    Energy32=[ 11.16,14.34,18.42,23.67,30.41,39.07,50.19,64.48,82.84,106.43,136.74,175.68,225.72,290.00,372.59,478.69, 615.01,790.16,1015.18,1304.28,1675.72,2152.93,   2766.05,   3553.77,   4565.82,  5866.09,  7536.64,  9682.94,  12440.47,  15983.28,  20535.04,  26383.05]

    energies = []

    for k in db.index:
        energy_list = []
        if db["Imod16"][k]:
            canalrange_max=canalmax_mod16
            canalrange_min=canalmin_mod16
            Energy=Energy16

        else:
            canalrange_max=canalmax_mod32
            canalrange_min=canalmin_mod32

            Energy=Energy32


        S=0
        M=0

        for canal in range(canalrange_min, canalrange_max+1):

             A=db['IE'+str(canal)][k] # A est donc le count d'ions pour ce canal d'énergie

             if A>seuil: # on fait la moyenne uniquement sur les canaux dont le count dépasse le seuil: l'idée c'est que pour déterminer le potentiel, il faut retirer ce qui n'est pas induit par le potentiel du satellite, donc tous le spectre qui est inférieur au seuil

                energy_list.append(Energy[canal - 1])
                S+=A
                M+=A*Energy[canal - 1] # on fait la moyenne des énergies pondérées par le count: il faut déterminer le potentiel, on pourrait prendre le canal qui a le maximum de coups en se disant que cela correspond directement au potentiel. on préfère faire une moyenne pondérée par le nombre de coups.

        if S != 0:
            M=-M/S
        else:
            M = None
        db['potentiel'][k]=M
        energies.append(energy_list)
    return energies






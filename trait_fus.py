from temps import temps

# nb_pas = args[4]


def trait_fus(tuple, nb_pas):
    """
    tuple = (liste_cas,datSort)

    On va considérer qu'un cas de charge peut occuper une durée de 10 min (ceci se justifie à partir du rapport AMBRE).
    """
    t_span = 600
    res = []
    times = []

    # dans une première étape, on fusionne les cas de charge qui correspondent au même cas de charge
    # le risque de fusionner deux cas de charge distincts est négligeable vue la rareté et l'éparpillement
    # des cas de charge

    for ls in tuple[0]:
        if ls != []:
            idx, tps = ls[0][0], ls[0][1]
            if times == [] or tps.duration(times[-1][1]) > t_span:
                times.append((idx,tps))

    # dans une seconde étape, on prend les données relatives au cas de charge en créant un nouveau dataframe.
    for :
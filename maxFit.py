from scipy.stats import maxwell

def maxFit(ncorr, Ereel):
    """
    Retourne un fit avec une seule maxwellienne.
    Simule une base de données à partir des valeurs des densités corrigées.
    Retourne les nombres utilisés.
    """
    n = len(Ereel)

    n0 = min(ncorr)
    data = []
    N = []
    for i in range(n):
        N.append(int(ncorr[i]/n0 + .5))
        for _ in range(N[i]):
            data.append(Ereel[i])
    return maxwell.fit(data), N

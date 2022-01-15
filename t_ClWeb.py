def jours_annee(n):
    n = int(n)
    if n in [2015, 2017, 2018, 2019, 2021] : return 365
    if n in [2016, 2020] : return 366
    raise ValueError("Année impossible : " + str(n))

def jours_mois(an, m):
    an = int(an)
    m = int(m)
    if m in [1, 3, 5, 7, 8, 10, 12] : return 31
    if m in [4, 6, 9, 11] : return 30
    if m == 2 and an in [2016, 2020] : return 29
    if m == 2 : return 28
    raise ValueError("Couple (an, mois) impossible : (" + str(an) + ", " + str(m) + ")")

def duree(date):  # On peut mettre ça comme un attribut
    """
    Permet de calculer la durée à partir du 1er janvier 2015 à  00:00:00.000 en secondes.
    C'est pour faciliter le calcul sur le temps
    """

    an = date[0]
    mois = date[1]
    jour = date[2]
    heure = date[3]
    min = date[4]
    sec = date[5]

    res = 0
    for n in range(2015, int(an)):
        res += jours_annee(n)
    for m in range(1, int(mois)):
        res += jours_mois(an, m)

    return sec + 60 * (min + 60 * (heure + 24 * (jour - 1 + res)))

class t_ClWeb:

    def __init__(self, string):
        jour = float(string[:2])
        mois = float(string[3:5])
        an = float(string[6:10])
        heure = float(string[11:13])
        min = float(string[14:16])
        sec = float(string[17:])
        self.a = [an, mois, jour, heure, min, sec]

    def ajouter(self, perio):  # OK
        T = duree(self.a) + perio

        self.a[0] = 2015
        while T >= jours_annee(self.a[0]) * 24 * 3600:
            T -= jours_annee(self.a[0]) * 24 * 3600
            self.a[0] += 1
        self.a[1] = 1
        while T >= jours_mois(self.a[0], self.a[1]) * 24 * 3600:
            T -= jours_mois(self.a[0], self.a[1]) * 24 * 3600
            self.a[1] += 1
        self.a[2] = 1 + T // (3600 * 24)
        T %= (3600 * 24)
        self.a[3] = T // 3600
        T %= 3600
        self.a[4] = T // 60
        T %= 60
        self.a[5] = T



    def __str__(self):  # OK
        self.a = [float(elt) for elt in self.a]
        res = ''

        for i in [2, 1, 0, 3, 4, 5]:
            c = str(self.a[i])
            if i < 5: c = c[:len(str(self.a[i])) - 2]
            if i not in [0, 5] and len(c) == 1: c = '0' + c
            if i == 5 and len(c) > 6: c = c[:6]
            res = res + c + ' '

        return res

    def __repr__(self):
        return self.__str__()
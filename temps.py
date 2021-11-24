"""
Cette classe permet une manipulation aisée du format du temps utilisé dans les fichier ASCII de ClWeb.
Elle permet d'implémenter le temps en secondes entre deux instants et une représentation visuelle des instants.
On s'en sert pour l'importation des données.
"""


def jours_annee(n):
    if n in [2015, 2017, 2018, 2019, 2021] : return 365
    if n in [2016, 2020] : return 366
    raise ValueError("Année impossible : " + str(n))

def jours_mois(an, m):
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

    an = int(date[:4])
    mois = int(date[5:7])
    jour = int(date[8:10])
    heure = int(date[11:13])
    min = int(date[14:16])
    sec = float(date[17:23])

    res = 0
    for n in range(2015, an):
        res += jours_annee(n)
    for m in range(1, mois):
        res += jours_mois(an, m)

    return sec + 60 * (min + 60 * (heure + 24 * (jour - 1 + res)))

class temps :

    def __init__(self, date):

        self.an = int(date[:4])
        self.mois = int(date[5:7])
        self.jour = int(date[8:10])
        self.heure = int(date[11:13])
        self.min = int(date[14:16])
        self.sec = float(date[17:23])

        self.duree = duree(date)


    def duration(self, t):
        return self.duree - t.duree

    def __str__(self):
        return str(self.an)+' '+str(self.mois)+" "+str(self.jour)+" "+str(self.heure)+":"+str(self.min)+":"+str(self.sec)

    def __repr__(self):
        return str(self.an)+' '+str(self.mois)+" "+str(self.jour)+" "+str(self.heure)+":"+str(self.min)+":"+str(self.sec)
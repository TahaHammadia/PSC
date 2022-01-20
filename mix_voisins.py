"""
Ce fichier facilite l'analyse des fichiers en éliminant les instants trop proches pour correspondre à deux phénomènes distincts.
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

class t:

    def __init__(self, string):

            self.a = []
            text = ''
            for c in string :
                if c in [':', ' ', '\n']:
                    self.a.append(float(text))
                    text = ''
                else:
                    text = text + c


    def __str__(self):

        res = ''

        for i in [2, 1, 0, 3, 4, 5]:
            c = str(self.a[i])
            if i < 5: c = c[:len(str(self.a[i])) - 2]
            if i not in [0, 5] and len(c) == 1: c = '0' + c
            res = res + c + ' '

        return res

    def __repr__(self):
        return self.__str__()

times = []
with open("C:/Users/hp 650 G3/Documents/GitHub/PSC/resultats.txt") as f:
    times = f.readlines()
times = [t(elt) for elt in times]
idx0 = 0
idx1 = 1
cpt = 0

with open("C:/Users/hp 650 G3/Documents/GitHub/PSC/resMayTa.txt", 'w') as f:
    f.write('')

while idx1 < len(times):
    if duree(times[idx1].a) > duree(times[idx0].a) + 30:
        with open("C:/Users/hp 650 G3/Documents/GitHub/PSC/resMayTa.txt", 'a') as f:
            f.writelines([str(times[idx0]) + '\n'])
            cpt += 1
        idx0 = idx1
        idx1 = idx0 + 1
    else:
        idx1 += 1
print(cpt)
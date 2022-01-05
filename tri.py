#nbr_vide = 10  # paramètre à ajuster

def Tri(dataset, nbr_vide):
    """
    Cette fonction sert à trier un dataframe pour trouver ensuite les évènements chargeants.
    Renvoie une liste d'indices des lignes du dataframe.
    Ces indices sont déterminés selon les critères suivants : la latitude (les pôles, en évitant l'Anomalie de l'Atlantique Sud), l'heure magnétique locale, et le nombre de canaux nuls en prenant en compte le mode.
    """
    Resultat=[]
    k=0
    Mod_16 = []
    for i in range(len(dataset)):

        invlat = float(dataset["INVLAT"][i])

        if  45<=invlat or invlat<=-60 :
            # On prend une valeur plus proche du pôle dans la région sud afin d'éviter l'anomalie SAA.

#             On convertit MLT s'il est de type str:
            if isinstance(dataset["MLT"][i], str):
                mlt=float(dataset["MLT"][i][:-1])
            else:
                mlt=dataset["MLT"][i]

            if mlt > 18 or mlt < 6 :  # à affiner


                n=0

                if dataset["mod16"][i]:
                    nbr_vide //= 2

                    for j in range(1,17):
                        if dataset["E"+str(j)][i]==0:
                            n+=1

                else:

                    for j in range(1,33):
                        if dataset["E"+str(j)][i]==0:
                            n+=1

                # Resultat.append(i)
                if n<=nbr_vide:
#                     on regarde le nombre de zéros,

                    Resultat.append(i)

    return Resultat
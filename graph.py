import matplotlib.pyplot as plt
import matplotlib.dates as dates

from datetime import datetime

def TracerActivXY(infos,min=0,max=-1):

    plt.figure(figsize=(12,7))

    if max>len(infos) or max<0:
        max=len(infos)

    t1,t2=True,True

    for j in range(1,33):

        for i in range(0,max-min):

            if infos['E'+str(j)][i+min]==2:

                if t2:

                    plt.plot([datetime.fromtimestamp(infos['Center_time'][i+min].duree+1420070400),datetime.fromtimestamp(infos['Center_time'][i+min].duree+0.3+1420070400)],[j,j], 'r', drawstyle='steps', linewidth='20', label="    Seuil supérieur")
                    t2=False

                else:

                    plt.plot([datetime.fromtimestamp(infos['Center_time'][i+min].duree+1420070400),datetime.fromtimestamp(infos['Center_time'][i+min].duree+0.3+1420070400)],[j,j], 'r', drawstyle='steps', linewidth='20')

            elif infos['E'+str(j)][i+min]==1:

                if t1:

                    plt.plot([datetime.fromtimestamp(infos['Center_time'][i+min].duree+1420070400),datetime.fromtimestamp(infos['Center_time'][i+min].duree+0.3+1420070400)],[j,j], 'g', drawstyle='steps', linewidth='20', label="    Seuil inférieur")
                    t1=False

                else:

                    plt.plot([datetime.fromtimestamp(infos['Center_time'][i+min].duree+1420070400),datetime.fromtimestamp(infos['Center_time'][i+min].duree+0.3+1420070400)],[j,j], 'g', drawstyle='steps', linewidth='20')

    plt.xlabel('Temps')
    plt.ylabel("Indice du canal d'énergie / Nombre de cas consecutifs")
    plt.title("Visualisation de l'analyse")
    # plt.legend(bbox_to_anchor=(1.05, 1))



def TracerCasConsec(infos,min=0,max=-1):

    if max>len(infos) or max<0:
        max=len(infos)

    x=[]

    for i in range(0,max-min-1):
        x.append(datetime.fromtimestamp(infos['Center_time'][i+min+1].duree+1420070400))

    plt.plot(x,infos['cas_consec'][min:max-1],drawstyle='steps', label="    Cas consécutifs")
    plt.legend(bbox_to_anchor=(1, 1))
    # plt.plot(x,infos['bug_consec'][min:max],drawstyle='steps')


def Traceboth(infos,min=0,max=-1):

   TracerActivXY(infos,min,max)
   TracerCasConsec(infos,min,max)
   plt.show()


def TraceAnalyseTest(dossier,args,min,max):
    Traceboth(Analyse2Dossier("1 jour mai",args),min,max)

def findindextime(instant,infos):
    i=0
    while i<len(infos) and datetime.fromtimestamp(infos['Center_time'][i].duree+1420070400)<instant:
        i+=1
    return i

def TracebothT(infos,instant_debut,instant_fin):
    min=findindextime(instant_debut,infos)
    max=findindextime(instant_fin,infos)
    TracerActivXY(infos,min,max)
    TracerCasConsec(infos,min,max)
    plt.show()

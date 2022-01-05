from sys import path

ad_may="A:/Travail/X/PSC/python"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

#ad=ad_may
ad=ad_taha

path.append(ad)

from temps import temps
from tri import Tri
from find import CasdeCharge2
from find import CasdeCharge3
from data import charge_ligne
import pandas as pd
import time
import os


def Analyse(n,fichier_ions,fichier_mlt,fichier_index,fichier_resultats, nb_canaux_max = 2, pas_bug = 4, nbr_vide = 10):
    """
    Récupère l'état de la recherche de cas chargeants dans fichier_index.
    Continue la recherche de cas chargeants en analysant n fois 100 000 lignes de fichier_ions et les lignes correspondantes de fichier_mlt.
    écris les instants détectés dans fichier_resultats et actualise fichier_index à chaque itération
    """

    t0=time.time()
    t2=t0

    # Récupérer l'état de la recherche de cas chargeants
    # iions est l'indice de la première ligne non analysée du fichier_ion, pareil pour imlt
    # Nions est le nombre de lignes du fichier_ion, idem pour Nmlt
    with open (fichier_index) as f:
        iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))

    for k in range(n):

        t1=time.time()

        # fions est la ligne de fin de l'itération
        # fmlt est une prédiction (car il faut une borne) de la fin de l'itération
        fions=min(Nions,iions+100000)
        fmlt=min(Nmlt,imlt+5000)

        # j le nombre de lignes de fichier_mlt parcourues lors de la construction de dat
        dat,j=charge_ligne(fichier_ions,fichier_mlt,iions,fions,imlt,fmlt)

        # datsort correspond à dat selectionné par Tri. Elle ne contient que des lignes qui peuvent contenir des cas de charge.
        datsort=dat.iloc[Tri(dat, nbr_vide)]


        # L est la liste des résultats de la détection de cas de charge.
        L=CasdeCharge(datsort, nb_canaux_max, pas_bug)
        del datsort


        # On écrit à la suite des résultats précédents les instants détectés dans fichier_resultats.
        with open(fichier_resultats,'a') as f:
            for cas in L:
                f.writelines([str(cas[1]),'\n'])

        # fmlt est actualisé pour avoir la valeur exacte de l'indice de fin de parcourt.
        fmlt=imlt+j

        # on actualise le fichier_index
        with open(fichier_index, 'w') as f:
            f.writelines([str(fions),'\n',str(fmlt),'\n',str(Nions),'\n',str(Nmlt)])

        # si on atteint la fin des fichiers, on s'arrete
        if fions==Nions or fmlt>=Nmlt:
            break

        # sinon on recommence avec pour indice de départ celui où on s'est arrêté.
        iions=fions
        imlt=fmlt

        t2=time.time()

        print(str(dat['Center_time'][len(dat)-1])+'   analyse '+str(k)+'   temps mis '+str(int((t2-t1)*100)/100)+'s')

        del dat

    print('\n Moyenne du temps d analyse de 100 000 lignes: '+str(int((t2-t0)/n*100)/100)+'s')

    # on renvoie l'indice de mlt où le parcourt s'est arrêté. Cela permet d'optimiser AnalyseSplit
    return(fmlt)

def Analyse_dossier(dossier, nb_canaux_max = 2, pas_bug = 4, nbr_vide = 10):
    """
    Permet d'analyser un dossier contenant le fichier obj5_Panel01_JASON3_AMBRE_P10_SC1.asc comme fichier_ion et obj7.asc comme fichier mlt.
    Crée automatiquement l'index et les résultats.
    Utile lorsqu'on télécharge directement les données depuis CLweb.
    """

    ud=ad+"data/"+dossier

    num_lines_ions = sum(1 for line in open(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"))
    num_lines_mlt = sum(1 for line in open(ud+"/obj7.asc"))

    with open(ud+"/index.txt", 'w') as f:
        f.writelines("1\n1\n"+str(num_lines_ions)+"\n"+str(num_lines_mlt))

    Analyse(num_lines_ions//100000+1,ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc",ud+"/obj7.asc",ud+"/index.txt",ud+"/resultats.txt", nb_canaux_max, pas_bug, nbr_vide)



def AnalyseSplit(dossier, n=12,l=14979648, nb_canaux_max = 2, pas_bug = 4, nbr_vide = 10):
    """
    dossier: dossier dans /data où se situent les fichiers
    n : nombre de fichiers obj5
    l : nombre de lignes par fichier obj5
    Cette fonction permet d'analyser un fichier_ions de grande taille découpé en plus petits par split de Git Bash.
    split "adresse du fichier" -l "nombre de lignes d'un fichier"
    """

    # Dans le cas d'un fichier obj5.asc de trop grosse taille, typiquement un fichier d'un an de 12Go
    # Il faut le split avec Git Bash en fichiers plus petits, de la taille d'un Go environ
    # On le divise en fichiers ayant un nombre de lignes max qui doit être divisible par 32 (par exemple 14979648) pour que les algorithmes puissent fonctionner correctement dessus
    # Ces fichiers sont renommés obj5 (i) avec i allant de 2 à 13
    # Le fichier obj7 n'a pas besoin d'être split
    # On créé un fichier index pour chaque obj5 (i), mais un seul fichier resultats


    ud=ad+"data/"+dossier
    num_lines_mlt = sum(1 for line in open(ud+"/obj7.asc"))
    num_lines_ions= l
    k=1

    for i in range(2,n+2):

        if i==n+1:
            num_lines_ions = sum(1 for line in open(ud+"/obj5 ("+str(i)+")"))


        index=ud+"/index"+str(i)+".txt" # ça commence à 2

        # si le fichier index n'existe pas, on le crée
        if not os.path.isfile(index):
            with open(index, 'w') as f:
                f.writelines("1\n"+str(k)+"\n"+str(num_lines_ions)+"\n"+str(num_lines_mlt))

        k=Analyse(num_lines_ions//100000+1,ud+"/obj5 ("+str(i)+")",ud+"/obj7.asc",index,ud+"/resultats.txt", nb_canaux_max, pas_bug, nbr_vide)




def Analyse2(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args=[500,200,1,3,5,5,26,2,14,2,14],printing=True):
    """
    Récupère l'état de la recherche de cas chargeants dans fichier_index.
    Continue la recherche de cas chargeants en analysant 100 000 lignes de fichier_ions et les lignes correspondantes de fichier_mlt.
    écris les instants détectés dans fichier_resultats et actualise fichier_index à chaque itération
    Utilise la version CasDeCharge2 avec args comme arguments
    """

    nbr_vide=args[10]

    t0=time.time()
    t2=t0

    # Récupérer l'état de la recherche de cas chargeants
    # iions est l'indice de la première ligne non analysée du fichier_ion, pareil pour imlt
    # Nions est le nombre de lignes du fichier_ion, idem pour Nmlt
    with open (fichier_index) as f:
        iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))


    # fions est la ligne de fin de l'itération
    # fmlt est une prédiction (car il faut une borne) de la fin de l'itération
    fions=min(Nions,iions+100000)
    fmlt=min(Nmlt,imlt+5000)

    # j le nombre de lignes de fichier_mlt parcourues lors de la construction de dat
    dat,j=charge_ligne(fichier_ions,fichier_mlt,iions,fions,imlt,fmlt)

    # datsort correspond à dat selectionné par Tri. Elle ne contient que des lignes qui peuvent contenir des cas de charge.
    datsort=dat.iloc[Tri(dat, nbr_vide)]


    # L est la liste des résultats de la détection de cas de charge.
    L,infos=CasdeCharge2(datsort, args)
    del datsort


    # On écrit à la suite des résultats précédents les instants détectés dans fichier_resultats.
    with open(fichier_resultats,'a') as f:
        for cas in L:
            f.writelines([str(cas[1]),'\n'])

    # fmlt est actualisé pour avoir la valeur exacte de l'indice de fin de parcourt.
    fmlt=imlt+j

    # on actualise le fichier_index
    with open(fichier_index, 'w') as f:
        f.writelines([str(fions),'\n',str(fmlt),'\n',str(Nions),'\n',str(Nmlt)])


    # sinon on recommence avec pour indice de départ celui où on s'est arrêté.
    iions=fions
    imlt=fmlt

    t2=time.time()

    if printing and len(dat)>0:
        print(str(dat['Center_time'][len(dat)-1])+'   analyse terminée,   temps mis '+str(int((t2-t0)*100)/100)+'s')

    del dat

    # on renvoie l'indice de mlt où le parcourt s'est arrêté. Cela permet d'optimiser AnalyseSplit. Ainsi que les infos recueillies
    return(fmlt,infos,len(L))
    # return fmlt,datsort


def Analyse2Dossier(dossier,args=[500,200,1,3,5,5,26,2,14,2,14]):
    """
    Permet d'analyser un dossier contenant le fichier obj5_Panel01_JASON3_AMBRE_P10_SC1.asc comme fichier_ion et obj7.asc comme fichier mlt.
    Se sert de l'algo CasDeCharge2 à travers Analyse2
    Crée automatiquement l'index et les résultats.
    Utile lorsqu'on télécharge directement les données depuis CLweb.
    """

    ud=ad+"/data/"+dossier

    num_lines_ions = sum(1 for line in open(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"))
    num_lines_mlt = sum(1 for line in open(ud+"/obj7.asc"))

    with open(ud+"/index.txt", 'w') as f:
        f.writelines("1\n1\n"+str(num_lines_ions)+"\n"+str(num_lines_mlt))

    infos=Analyse2(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc",ud+"/obj7.asc",ud+"/index.txt",ud+"/resultats.txt",args)[1]

    for i in range(1,num_lines_ions//100000+1):
        k,S, n=Analyse2(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc",ud+"/obj7.asc",ud+"/index.txt",ud+"/resultats.txt",args)
        infos.append(S)

    return infos


def Analyse2Test(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args):
    res = Analyse2(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args,False)[1:]
    with open (fichier_index) as f:
        iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))
    with open(fichier_index, 'w') as f:
        f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])
    return (res[0], res[1] > 0)


def Analyse2Split(dossier, args, n=12,l=14979648):

    ud=ad+"/data/"+dossier
    num_lines_mlt = sum(1 for line in open(ud+"/obj7.asc"))
    num_lines_ions= l
    k=1

    for i in range(2,n+2):

        if i==n+1:
            num_lines_ions = sum(1 for line in open(ud+"/obj5 ("+str(i)+")"))


        index=ud+"/index"+str(i)+".txt" # ça commence à 2

        # si le fichier index n'existe pas, on le crée
        if not os.path.isfile(index):
            with open(index, 'w') as f:
                f.writelines("1\n"+str(k)+"\n"+str(num_lines_ions)+"\n"+str(num_lines_mlt))

        for j in range(num_lines_ions//100000+1):

            k,infos,L=Analyse2(ud+"/obj5 ("+str(i)+")",ud+"/obj7.asc",index,ud+"/resultats.txt", args)
            if len(infos)==0:
                break
            del infos


def Analyse3(fichier_ions,fichier_mlt,fichier_index, args=[500,200,1,3,5,5,26,2,14,2,14],printing=True):
    """
    Récupère l'état de la recherche de cas chargeants dans fichier_index.
    Continue la recherche de cas chargeants en analysant 100 000 lignes de fichier_ions et les lignes correspondantes de fichier_mlt.
    écris les instants détectés dans fichier_resultats et actualise fichier_index à chaque itération
    Utilise la version CasDeCharge2 avec args comme arguments
    """

    nbr_vide=args[10]

    t0=time.time()
    t2=t0

    # Récupérer l'état de la recherche de cas chargeants
    # iions est l'indice de la première ligne non analysée du fichier_ion, pareil pour imlt
    # Nions est le nombre de lignes du fichier_ion, idem pour Nmlt
    with open (fichier_index) as f:
        iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))


    # fions est la ligne de fin de l'itération
    # fmlt est une prédiction (car il faut une borne) de la fin de l'itération
    fions=min(Nions,iions+100000)
    fmlt=min(Nmlt,imlt+5000)

    # j le nombre de lignes de fichier_mlt parcourues lors de la construction de dat
    dat,j=charge_ligne(fichier_ions,fichier_mlt,iions,fions,imlt,fmlt)

    # datsort correspond à dat selectionné par Tri. Elle ne contient que des lignes qui peuvent contenir des cas de charge.
    datsort=dat.iloc[Tri(dat, nbr_vide)]


    # L est la liste des résultats de la détection de cas de charge.
    infos=CasdeCharge3(datsort, args)
    del datsort



    # fmlt est actualisé pour avoir la valeur exacte de l'indice de fin de parcourt.
    fmlt=imlt+j

    # on actualise le fichier_index
    with open(fichier_index, 'w') as f:
        f.writelines([str(fions),'\n',str(fmlt),'\n',str(Nions),'\n',str(Nmlt)])


    # sinon on recommence avec pour indice de départ celui où on s'est arrêté.
    iions=fions
    imlt=fmlt

    t2=time.time()

    if printing and len(dat)>0:
        print(str(dat['Center_time'][len(dat)-1])+'   analyse terminée,   temps mis '+str(int((t2-t0)*100)/100)+'s')

    del dat

    # on renvoie l'indice de mlt où le parcourt s'est arrêté. Cela permet d'optimiser AnalyseSplit. Ainsi que les infos recueillies
    return(fmlt,infos)

def Analyse3Dossier(dossier,args=[500,200,1,3,5,5,26,2,14,2,14]):
    """
    Permet d'analyser un dossier contenant le fichier obj5_Panel01_JASON3_AMBRE_P10_SC1.asc comme fichier_ion et obj7.asc comme fichier mlt.
    Se sert de l'algo CasDeCharge2 à travers Analyse2
    Crée automatiquement l'index et les résultats.
    Utile lorsqu'on télécharge directement les données depuis CLweb.
    """

    ud=ad+"/data/"+dossier

    num_lines_ions = sum(1 for line in open(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"))
    num_lines_mlt = sum(1 for line in open(ud+"/obj7.asc"))

    with open(ud+"/index.txt", 'w') as f:
        f.writelines("1\n1\n"+str(num_lines_ions)+"\n"+str(num_lines_mlt))

    infos=Analyse3(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc",ud+"/obj7.asc",ud+"/index.txt",args)[1]

    for i in range(1,num_lines_ions//100000+1):
        k,S=Analyse3(ud+"/obj5_Panel01_JASON3_AMBRE_P10_SC1.asc",ud+"/obj7.asc",ud+"/index.txt",ud+"/resultats.txt",args)
        infos = infos.append(S, ignore_index=True)

    return infos
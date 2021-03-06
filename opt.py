from sys import path
from numpy import random

ad_may="A:/Travail/X/PSC/python"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

ad=ad_may
# ad=ad_taha

path.append(ad)
from main import Analyse2Test

setSeuilActif = [i for i in range(100, 1010, 10)] # seuil_actif
setSeuilInactif = [j for j in range(0, 600, 10)]# seuil inactif
# setCanauxMin = [i for i in range(1, 4)]
setCanauxMax = [j for j in range(2, 6)]
setPas = [i for i in range(3, 10)] # nb_pas
setBug = [j for j in range(2, 9)]  #pas_bug
#setMod32 = [(i,j) for i in range(24, 33) for j in range(1, min(i, 8))] # canalmax_mod32, canalmin_mod32
#setMod16 = [(i,j) for i in range(12, 17) for j in range(1, min(i, 4))] # canalmax_mod16, canalmin_mod16
# setVide = [i for i in range(7, 16)] # nbr_vide

pasid = [30, 30, 1, 3, 3]
lset = [setSeuilActif, setSeuilInactif, setCanauxMax, setPas, setBug]
default = 1, 3, 32, 3, 16, 3, 15

ud0 = ad+"/File[0]/"
ud1 = ad+"/File[1]/"

f_ions = "obj5_Panel01_JASON3_AMBRE_P10_SC1.asc"
f_mlt = "obj7.asc"
f_idx = "indice.txt"
f_res = "resultat.txt"

alpha = 0.3

files0 = list([tuple(ud0 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["16_04_2017_16.56/", "16_07_2017_01.13/", "16_07_2017_19.29/", "17_09_2019_08.57/", "02_05_2016_15.06/", "28_03_2016_19.07/", "05_04_2016_16.22/", "05_04_2016_18.16/", "27_04_2016_13.14/", "01_05_2016_20.22/", "03_01_2020_07.19/", "05_01_2020_00.30/", "25_03_2020_11.38/", "25_06_2020_18.24/", "25_06_2020_18.26/", "27_06_2018_20.14/", "10_11_2017_18.27/", "15_02_2018_16.50/", "14_08_2017_13.12/", "27_01_2018_00.45/"]])

files1 = list([tuple(ud1 + dat + f for f in [f_ions, f_mlt, f_idx, f_res]) for dat in ["20_10_2017_02.41/", "28_01_2018_01.06/", "28_05_2017_4.38/", "31_10_2019_00.02/", "01_01_2017_05.14/", "13_06_2018_22.41/", "13_06_2018_22.51/", "27_09_2019_01.09/", "03_06_2017/", "07_03_2017/", "09_04_2017/", "09_12_2017/", "14_10_2017/", "19_05_2017/", "21_03_2017/", "21_04_2017/", "21_11_2017/", "25_10_2017/", "28_05_2017/", "02_11_2017_00.38/", "02_11_2017_23.03/", "04_04_2017_08.39/", "05_03_2017_18.24/", "05_09_2017_02.25/", "05_09_2017_09.51/", "06_02_2018_05.01/"]])

files = [files0, files1]

lossDict = {}

def init():
    
    for file in files0 + files1:
        Nions = sum(1 for line in open(file[0]))
        Nmlt = sum(1 for line in open(file[1]))
        with open(file[2], 'w') as f:
            f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])
            
    with open(ad+"/res.txt", 'a') as f:
        f.writelines(["___________________________", '\n'])

def Args(idarg):
    return [setSeuilActif[idarg[0]], setSeuilInactif[idarg[1]], default[0], setCanauxMax[idarg[2]], setPas[idarg[3]], setBug[idarg[4]], default[2], default[3], default[4], default[5], default[6]]


def loss(idarg, files):
    """
    files est un tuple ou liste dont le premier ??l??ment est une liste de cas de charges et le second une liste de non cas de charges.
    """
    args = Args(idarg)
    
    try :

        res =  lossDict[str(idarg[0]) + "_" + str(idarg[1]) + "_" + str(idarg[2]) + "_" + str(idarg[3]) + "_" + str(idarg[4])]

    except KeyError:
        N = (len(files[0]) + len(files[1])) / 2
        cpt = [0, 0]

        for i in range(2):
            for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in files[i] :
                if Analyse2Test(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args)[1]: cpt[i] += 1

        if cpt[0] == 0: val = float('inf')

        else: val = (len(files[0]) - cpt[0] + alpha * cpt[1]) / N

        res = val, (len(files[0]) - cpt[0]) / N, cpt[1] / N
        lossDict[str(idarg[0]) + "_" + str(idarg[1]) + "_" + str(idarg[2]) + "_" + str(idarg[3]) + "_" + str(idarg[4])] = res
    if res[0]==float('inf'): print(args, 'inf', int(1000*res[1])/1000, int(1000*res[2])/1000)
    else: print(args, int(1000*res[0])/1000, int(1000*res[1])/1000, int(1000*res[2])/1000)
    return res[0]
    
    
def next(idarg, pasid, lossValue):
    
    l=lossValue
    j=-1
    d=0
    
    for i in range(len(idarg)):
        
        A=idarg.copy()
        A[i]+=pasid[i]
        
        if A[i]<len(lset[i]) and setSeuilActif[A[0]]>setSeuilInactif[A[1]] and setBug[A[4]]<=setPas[A[3]]:
            
            m=loss(A, files)
            
            if m<l:
                l=m
                j=i
                d=1
        
        A[i]-=2*pasid[i]
        
        if A[i]>=0 and setSeuilActif[A[0]]>setSeuilInactif[A[1]] and setBug[A[4]]<=setPas[A[3]]:
            
            m=loss(A, files)
            
            if m<l:
                l=m
                j=i
                d=-1
    
    if d==0:

        
        for i in range(len(idarg)):
            
            if pasid[i] != 1:
                pasid[i]=abs(pasid[i]//2)
        
        print("R??duction du pas : "+str(pasid))
        
        return (idarg,pasid,lossValue)
    
    else:
        
        idarg[j]+=d*pasid[j]
        
        print("Progression au point : "+str(Args(idarg)))
        
        return(idarg,pasid,l)
    
    
def opt_int(idarg, lossValue = float('inf'), pas = pasid.copy()):
    chemin = [(idarg, lossValue)]
    idarg0, lossValue0, pas0 = idarg.copy(), lossValue, pas.copy()
    for file in files[0] + files[1]:
        with open (file[2]) as f:
            iions,imlt,Nions,Nmlt = list(map(int, f.readlines()))
        with open(file[2], 'w') as f:
            f.writelines(['1','\n','1','\n',str(Nions),'\n',str(Nmlt)])
    k = 2
    while k > 1:
        idarg, pas, lossValue = next(idarg, pas, lossValue)
        chemin.append((idarg.copy(), lossValue))
        k = pas[0] * pas[1] * pas[2] * pas[3] * pas[4]
    res = idarg, lossValue, pas
    with open(ad+"/res.txt", 'a') as f:
        f.write(str(idarg0) + ' ' + str(lossValue0) + ' ' + str(pas0) + ' :: ' + str(idarg) + ' ' + str(lossValue) + ' ' + str(pas) + str(lossValue) + '\n')
    return res, chemin

max_beg = [len(setSeuilActif) - 1, 0, len(setPas) - 1, 0, 0]

# init()
# print(opt_int([74, 7, 0, 1, 0, 0, 1], pas = [1] * 7))

# args = [seuil_actif, seuil_inactif, nb_canaux_min, nb_canaux_max, nb_pas, pas_bug, canalmax_mod32, canalmin_mod32, canalmax_mod16, canalmin_mod16, nbr_vide]

def testrandom(tpas):
    
    idarg=[]
    
    for Set in lset:
        
        idarg.append(random.randint(len(Set)))
        
    while setSeuilActif[idarg[0]]<setSeuilInactif[idarg[1]] or setBug[idarg[4]]>setPas[idarg[3]]:
        
        idarg=[]
        
        for Set in lset:
            
            idarg.append(random.randint(len(Set)))
    
    init()
    tpas[0]+=(random.randint(2)-1)*random.randint(5)
    tpas[1]+=(random.randint(2)-1)*random.randint(5)
    tpas[4]+=(random.randint(2)-1)
    # tpas[5]+=(random.randint(2)-1)
    # tpas[6]+=(random.randint(2)-1)
    print(opt_int(idarg,pas=tpas.copy()))


def grapharg(idarg,i=0):
    
    args=Args(idarg)
    
    for fichier_ions,fichier_mlt,fichier_index,fichier_resultats in files[i] :
        infos=Analyse2Test(fichier_ions,fichier_mlt,fichier_index,fichier_resultats, args)[0]
        if len(infos)==0:
            print('Erreur info vide : '+str(fichier_index))
        else:
            Traceboth(infos)

for k in range(50):
    testrandom(pasid.copy())
    
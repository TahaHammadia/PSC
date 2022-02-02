from math import sqrt

K=sqrt(9.1*10**(-31))*10**6/(sqrt(2)*16*10**(-3)*1.5*10**(-4))
e=1.6*10**(-19)

Energy16=[ 12.65,   20.88,      34.46,    56.89,   93.90,     154.99,    255.85,   422.32,   697.10,   1150.69,   1899.40,   3135.27,  5175.28,  8542.65,  14101.05,  23276.10] #Ce sont les énergies des canaux, on les a dans les fichiers ascii

Energy32=[ 11.16,14.34,18.42,23.67,30.41,39.07,50.19,64.48,82.84,106.43,136.74,175.68,225.72,290.00,372.59,478.69, 615.01,790.16,1015.18,1304.28,1675.72,2152.93,   2766.05,   3553.77,   4565.82,  5866.09,  7536.64,  9682.94,  12440.47,  15983.28,  20535.04,  26383.05]

DeltaE16=[]

DeltaE32



def distrib_corr(liste_count_electr,potentiel,mod16):

    L=liste_count_electr.copy()
    ncorr=[]
    Ereel=[]

    if mod16:
        Energy=Energy16
        DeltaE=DeltaE16
        N=16
    else:
        Energy=Energy32
        DeltaE=DeltaE32
        N=32

    for i in range(N):
        ncorr.append(K*L[i]/(sqrt(Energy[i])*DeltaE[i]))
        Ereel.append(Enertg[i]-e*potentiel)

    return ncorr,Ereel






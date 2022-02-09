from math import sqrt
from math import pi

K=4*pi*sqrt(9.1*10**(-31))/(sqrt(2)*16*10**(-3)*1.5*10**(-8))
e=1.6*10**(-19)

Energy16=[ 12.65,   20.88,      34.46,    56.89,   93.90,     154.99,    255.85,   422.32,   697.10,   1150.69,   1899.40,   3135.27,  5175.28,  8542.65,  14101.05,  23276.10] #Ce sont les énergies des canaux, on les a dans les fichiers ascii

Energy32=[ 11.16,14.34,18.42,23.67,30.41,39.07,50.19,64.48,82.84,106.43,136.74,175.68,225.72,290.00,372.59,478.69, 615.01,790.16,1015.18,1304.28,1675.72,2152.93,   2766.05,   3553.77,   4565.82,  5866.09,  7536.64,  9682.94,  12440.47,  15983.28,  20535.04,  26383.05]

DeltaE16=[6.25, 10.57, 17.45, 28.81, 47.55, 78.49, 129.57, 213.88, 353.04, 582.76, 961.93, 1587.82, 2620.97, 4326.34, 7141.34, 11323.22]

DeltaE32=[2.65,3.60, 4.63, 5.95, 7.64, 9.81, 12.61, 16.20, 20.82, 26.74, 34.35, 44.14, 56.71, 72.86, 93.61, 120.26, 154.52, 198.53, 255.06, 327.69, 421.02, 540.91, 694.96, 892.87, 1147.14, 1473.82, 1893.54, 2432.79, 3125.61, 4015.73, 5159.34, 6163.89]



def distrib_corr(liste_count_electr,potentiel,mod16):
    '''
    Cette fonction détermine la distribution des électrons suivant leur énergie.
    Elle renvoie deux listes: la liste des valeurs de la distribution et la liste des énergies de ces valeurs, ie [n(E)] et [E].
    Pour calculer cette distribution on doit corriger l'effet du potentiel du satellite et transformer le flux en distribution.
    '''
    if potentiel!=None:

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
            ncorr.append(K*L[i]/(sqrt(Energy[i]*e)*Energy[i]))
            Ereel.append(Enertg[i]-e*potentiel)

        return ncorr,Ereel

    else:

        return [],[]

# nous avons accès au nombre d'électrons dans une plage d'énergie qui heurtent le détecteur durant une durée de mesure dt.
# ce nombre est noté z(E1) où E1 est l'énergie cinétique qu'à l'électron quand il frappe le détecteur
# on a donc z(E1)=4pi*dt*surface_eff*dE1*v(E1)*n(E) avec v la vitesse de l'électron et E l'énergie cinétique initiale de l'électron
# ainsi E=E1-eU avec U le potentiel du satellite
# et E1=1/2*m*v^2
#
# on a un facteur donné par le constructeur gef=surface_eff*dE1/E1
# finalement n(E)=z(E1)/(sqrt(E1)*E1)*sqrt(m)/(sqrt(2)*dt*gef)
# donc n(E)=K*z(E1)/(sqrt(E1)*dE1)
# avec K=sqrt(m)/(sqrt(2)*dt*surface)
# il y a un facteur 10**6 en plus dans le K venant du fait que la z=10**6 * mesure ambre




import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def plotdistrib(n,E):



    plt.figure(figsize=(12,7))

    a=min(1,0.3*1000/len(n))

    plt.scatter(E,n, alpha=a)
    plt.yscale('log')
    plt.xscale('log')

    plt.xlabel('Energie')
    plt.ylabel('Distribution des électrons')

    plt.show()

def animatedistrib(dist):

    j=18
    while len(dist['n'][j])==0:
        j+=1

    fig=plt.figure(figsize=(12,7))
    linen, = plt.plot(dist['E'][j],dist['n'][j])
    lineU, = plt.plot([-dist['U'][j],-dist['U'][j]],[0,10**3])


    # title=str(dist['Center_time'][j].heure)+'h'+str(dist['Center_time'][j].min)+':'+str(int(dist['Center_time'][j].sec))+'  '+str(dist['Center_time'][j].jour)+'/'+str(dist['Center_time'][j].mois)+'/'+str(dist['Center_time'][j].an)


    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energie')
    plt.ylabel('Distribution des électrons')


    def animate2(i):
        # print(i)
        k1=0
        while i//10+j+k1<len(dist) and len(dist['n'][i//10+j+k1])==0:
            k1+=1
        if i//10+j+k1<len(dist):

            k2=k1+1
            while i//10+j+k2<len(dist) and len(dist['n'][i//10+j+k2])==0:
                k2+=1
            if i//10+j+k2<len(dist):

                # print(k1,k2)
                # print(i//10+j+k1,i//10+j+k2)
                # print(i%10,10-i%10)


                n1=np.array(dist['n'][i//10+j+k1])
                E1=np.array(dist['E'][i//10+j+k1])
                U1=dist['U'][i//10+j+k1]

                n2=np.array(dist['n'][i//10+j+k2])
                E2=np.array(dist['E'][i//10+j+k2])
                U2=dist['U'][i//10+j+k2]
                # print(E1,n1)

                E=(E1*(10-i%10)+E2*(i%10))/10
                n=(n1*(10-i%10)+n2*(i%10))/10
                U=(U1*(10-i%10)+U2*(i%10))/10

                # print(E1[-1],E2[-1],E[-1])

                linen.set_xdata(E)
                linen.set_ydata(n)

                lineU.set_xdata([-U,-U])

                # title=str(dist['Center_time'][i//10+j+k1].heure)+'h'+str(dist['Center_time'][i//10+j+k1].min)+':'+str(int(dist['Center_time'][i//10+j+k1].sec))+'  '+str(dist['Center_time'][i//10+j+k1].jour)+'/'+str(dist['Center_time'][i//10+j+k1].mois)+'/'+str(dist['Center_time'][i//10+j+k1].an)




                if len(n1)!=0 and len(n2)!=0:

                    return linen, lineU

        return linen,lineU

    def animate1(i):
        n=dist['n'][i+j]
        E=dist['E'][i+j]
        line.set_xdata(E)
        line.set_ydata(n)
        return line,

    # ani=animation.FuncAnimation(fig, animate1, frames=len(dist)-j, blit=True, interval=500, repeat=False)
    ani=animation.FuncAnimation(fig, animate2, frames=10*(len(dist)-j), blit=True, interval=50, repeat=False)

    plt.show()
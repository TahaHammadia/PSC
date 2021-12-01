import matplotlib.pyplot as plt

def TracerInfos(infos,min=0,max=-1):

    if max>len(infos) or max<0:
        max=len(infos)

    for j in range(1,33):

        # L1,L2=(max-min)*[0],(max-min)*[0]
        Y1,Y2,X1,X2=[],[],[],[]

        for i in range(1,max-min):
            if infos['E'+str(j)][i+min]==2:
                X2.append
                L2[i]=j
            elif infos['E'+str(j)][i+min]==1:
                L1[i]=j

        plt.plot(L2, 'g', drawstyle='steps')
        plt.plot(L1, 'r', drawstyle='steps')

    plt.show()
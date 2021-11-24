import matplotlib.pyplot as plt

def TracerInfos(infos):

    for j in range(1,33):

        L1,L2=len(infos)*[0],len(infos)*[0]

        for i in range(len(infos)):
            if infos['E'+str(j)][i]==2:
                L2[i]=j
            elif infos['E'+str(j)][i]==1:
                L1[i]=j

        plt.plot(L2, 'g')
        plt.plot(L1, 'r')

    plt.show()
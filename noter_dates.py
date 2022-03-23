import os

file = "C:/Users/hp 650 G3/Documents/GitHub/PSC/data/Pics [11, 6, 2, 1, 1] [210, 60, 1, 4, 4, 3, 28, 3, 14, 3, 15]/dates.txt"

with open(file, 'w') as f:
    for pic in os.listdir(folder1)[2:]:
        f.write(pic[4:27])
        f.write('\n')

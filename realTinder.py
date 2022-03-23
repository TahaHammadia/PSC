from shutil import move
import os
from PIL import Image

print("Écrivez 1 si vous pensez qu'il s'agit d'un cas de charge, 0 sinon. Si vous voulez finir, écriver -1.")

folder2 = "C:/Users/hp 650 G3/Documents/GitHub/PSC/data/Pics/"
folder1 = "C:/Users/hp 650 G3/Documents/GitHub/PSC/data/Pics [11, 6, 2, 1, 1] [210, 60, 1, 4, 4, 3, 28, 3, 14, 3, 15]/"

with open(folder1 + "etat.txt", 'r') as f:
    cpt = int(f.readline())

for pic in os.listdir(folder1)[cpt:]:
    imageLue = Image.open(folder1 + pic)
    imageLue.show()
    jugement = input(" ")
    if jugement == '1':
        move(folder1 + pic, folder2 + pic)
    elif jugement == '0':
        cpt += 1
    elif jugement == '-1':
        with open(folder1 + 'etat.txt', 'w') as g:
            g.write(str(cpt))
        break
    else:
        with open(folder1 + 'etat.txt', 'w') as g:
            g.write(str(cpt))
        raise(ValueError("Valeur de jugement incorrecte"))


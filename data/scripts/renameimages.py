# rename images

import os

dir = r'C:\Users\paro\Coding Projects\SpellCastSolver\data\trainfiles'

images = [f for f in os.listdir(dir)if f.endswith('.png')]
print(f"{len(images)} number of images found")
lang = 'eng'
font = 'discord'
part1 = f"{lang}.{font}.exp"
for i, image in enumerate(images):
    filename = f"{part1}{i}.{image[-3:]}"
    print(filename)
    os.rename(os.path.join(dir, image), os.path.join(dir, filename))


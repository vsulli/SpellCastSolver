# removes all previous training and log files

import os

srcdir = r'C:\Users\paro\Coding Projects\SpellCastSolver\data\trainfiles'
destdir = r'C:\Users\paro\Coding Projects\SpellCastSolver\data\trainoutput'
files = os.listdir(srcdir)

for item in files:
    if not item.endswith(('.png', '.box')):
        os.remove(os.path.join(srcdir, item))

files = os.listdir(destdir)
for item in files:
    os.remove(os.path.join(destdir, item))

    


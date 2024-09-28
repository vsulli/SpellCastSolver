# create box files for images
import os

os.chdir(r'C:\Users\paro\Coding Projects\SpellCastSolver\data\trainfiles')

number_of_files = len(os.listdir('./'))
for i in range(0, number_of_files):
    os.system(f"tesseract eng.discord.exp{i}.png eng.discord.exp{i} batch.nochop makebox")


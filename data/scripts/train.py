# training
#TODO - reread article on this process

import os
import subprocess

srcdir = 'C:/Users/paro/Coding Projects/SpellCastSolver/data'
destdir = 'C:/Users/paro/Coding Projects/SpellCastSolver/data/trainfiles'


# generating the tuples of filenames
files = os.listdir(srcdir)
pngs = [x for x in files if x.endswith('.png')]
boxes = [x for x in files if x.endswith('.box')]
trainfiles = list(zip(pngs, boxes))


'''
# generating TR files and unicode character extraction
unicharset = f"unicharset_extractor -- output_unicharset ../../{destdir}/unicharset "
unicharset_args = f""
errorfiles = []
for image, box in trainfiles:
    unicharset_args += f"{box} "
    if os.path.isfile(f"{destdir}/{image[:-4]}.tr"):
        continue
    try:
        print(image)
        os.system(f"tesseract {srcdir}/{image} {destdir}/{image[:-4]} nobatch box.train")
    except:
        errorfiles.append((image, box))
os.chdir(srcdir)
subprocess.run(unicharset+unicharset_args)
os.chdir('../../')

# Creating font properties file
# fontname, italic, bold, fixed, serif, fraktur
with open(f"{destdir}/font_properties", 'w') as f:
    f.write("discord 0 0 0 0 0")

# # Getting all .tr files and training
output = r'C:\Users\paro\Coding Projects\SpellCastSolver\data\trainoutput'
trfiles = [f for f in os.listdir(destdir) if f.endswith('.tr')]
os.chdir(destdir)
mftraining = f"mftraining -F font_properties -U unicharset -O {output}/eng.unicharset -D {output}"
cntraining = f"cntraining -D {output}"
for file in trfiles:
    mftraining += f" {file}"
    cntraining += f" {file}"
subprocess.run(mftraining)
subprocess.run(cntraining)
os.chdir('../../')

# # Renaming training files and merging them
os.chdir(output[6:])
os.rename('inttemp', 'eng.inttemp')
os.rename('normproto', 'eng.normproto')
os.rename('pffmtable', 'eng.pffmtable')
os.rename('shapetable', 'eng.shapetable')
os.system(f"combine_tessdata eng.")

# Writing log file
if len(errorfiles) == 0:
    errorfiles.append(('no', 'Error'))
with open('tesseract/scripts/logs.txt', 'w') as f:
    f.write('\n'.join('%s %s' % x for x in errorfiles))

    '''


from functions import *
from pathlib import Path
import os
import shutil

scr_dir = '.'

Path(f"{scr_dir}/tmpOBJs").mkdir(parents=True, exist_ok=True)
Path("tmpFrames").mkdir(parents=True, exist_ok=True)

box      = {'ymin' : -6,'ymax' : 6, 
            'xmin' : -6,'xmax' : 6, 
            'zmin' : -6,'zmax' : 6 } 

dxyz = 0.15

#Molecule = psi4.geometry("""
#         H            0.34     0.0000    0.000000000000    
#         H           -0.34     0.0000     0.000000000000    
#""")

#Molecule = psi4.core.Molecule.from_string(open('OMeOMe-S0-ccpVTZ.xyz').read())
Molecule = psi4.core.Molecule.from_string(open('tet.xyz').read())

Nframes = 251

HOMO, LUMO, dx = generate_orbital_arrays(Molecule, box, dxyz)
genOBJs(HOMO,LUMO, dxyz, Nframes)
os.system(f'blender MaterialData.blend -b --python phased_frames.py {Nframes}')



for i in range(0,249):
 inp = (f'tmpFrames/{i}.png')
 out = (f'tmpFrames/{2*(Nframes-2)-i}.png')
 shutil.copyfile(inp,out)


os.system(f'ffmpeg -i tmpFrames/%d.png -c:v libx264 -pix_fmt yuv420p MOVIE.mp4 ')

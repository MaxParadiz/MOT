#!/usr/bin/python

from functions import *
from pathlib import Path
import os
import shutil

scr_dir = '.'
objFolder = f'{scr_dir}/OBJs'
frameFolder = f'{scr_dir}/Frames'

Path(objFolder).mkdir(parents=True, exist_ok=True)
Path(frameFolder).mkdir(parents=True, exist_ok=True)

box      = {'ymin' : -6,'ymax' : 6, 
            'xmin' : -6,'xmax' : 6, 
            'zmin' : -6,'zmax' : 6 } 

dxyz = 0.15

Molecule = psi4.geometry("""
         H            0.34     0.0000    0.000000000000    
         H           -0.34     0.0000     0.000000000000    
""")

#Molecule = psi4.core.Molecule.from_string(open('Geometry.xyz').read())

Nframes = 251

HOMO, LUMO, dx = generate_orbital_arrays(Molecule, box, dxyz)
genOBJs(HOMO,LUMO, dxyz, Nframes, objFolder)
os.system(f'blender $MOT/MaterialData.blend -b --python $MOT/create_frames.py {Nframes}')



for i in range(0,249):
 inp = (f'{frameFolder}/{i}.png')
 out = (f'{frameFolder}/{2*(Nframes-2)-i}.png')
 shutil.copyfile(inp,out)


os.system(f'ffmpeg -i {frameFolder}/%d.png -c:v libx264 -pix_fmt yuv420p MOVIE.mp4 ')

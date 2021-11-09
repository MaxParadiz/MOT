from functions import *
from pathlib import Path
import os

scr_dir = '.'
objFolder = f'{scr_dir}/OBJs'
frameFolder = f'{scr_dir}/Frames'
miscFolder = f'{scr_dir}/misc'

Path(objFolder).mkdir(parents=True, exist_ok=True)
Path(frameFolder).mkdir(parents=True, exist_ok=True)
Path(miscFolder).mkdir(parents=True, exist_ok=True)

box      = {'ymin' : -6,'ymax' : 6, 
            'xmin' : -6,'xmax' : 6, 
            'zmin' : -6,'zmax' : 6 } 

dxyz = 0.15


Molecule = psi4.geometry("""
         H            0.34     0.0000    0.000000000000    
         H           -0.34     0.0000     0.000000000000    
""")


#Molecule = psi4.core.Molecule.from_string(open('Geometry.xyz').read())

Nframes = 1

HOMO, LUMO, dx = generate_orbital_arrays(Molecule, box, dxyz, miscFolder)

genOBJs(HOMO,LUMO, dxyz, Nframes, objFolder)

os.system(f'blender $MOT/MaterialData.blend --python $MOT/view.py')

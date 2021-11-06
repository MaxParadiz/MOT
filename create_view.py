from functions import *
from pathlib import Path
import os

scr_dir = '.'

Path(f"{scr_dir}/tmpOBJs").mkdir(parents=True, exist_ok=True)
Path("tmpFrames").mkdir(parents=True, exist_ok=True)

box      = {'ymin' : -6,'ymax' : 6, 
            'xmin' : -6,'xmax' : 6, 
            'zmin' : -6,'zmax' : 6 } 

dxyz = 0.15


Molecule = psi4.core.Molecule.from_string(open('OMeOMe-S0-ccpVTZ.xyz').read())

Nframes = 1

HOMO, LUMO, dx = generate_orbital_arrays(Molecule, box, dxyz)
genOBJs(HOMO,LUMO, dxyz, Nframes)
os.system(f'blender MaterialData.blend --python view.py')

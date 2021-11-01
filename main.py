from functions import *
from pathlib import Path
import os

Path("tmpOBJs").mkdir(parents=True, exist_ok=True)
Path("tmpFrames").mkdir(parents=True, exist_ok=True)



Molecule = psi4.geometry("""
         H            0.34     0.0000    0.000000000000    
         H           -0.34     0.0000     0.000000000000    
""")

Nframes = 251

HOMO, LUMO, dx = generate_orbital_arrays(Molecule)
genOBJs(HOMO,LUMO, dx, Nframes)
os.system(f'blender MaterialData.blend -b --python phased_frames.py {Nframes}')
#

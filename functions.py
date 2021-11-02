import psi4
import numpy as np
from skimage import measure

#Molecule = psi4.core.Molecule.from_string(open('Formaldehyde.xyz').read())



def generate_orbital_arrays(Molecule,box, dxyz, orbs = []):
    # Compute the DFT energy and the wave function using the B3LYP functional and the cc-pVTZ basis
    
#    E, Wavefunction = psi4.energy('B3LYP/cc-pVTZ', molecule=Molecule, return_wfn=True)
    E, Wavefunction = psi4.energy('SCF/STO-3G', molecule=Molecule, return_wfn=True)
    
    # Get the number of "alpha" electrons to find the HOMO and LUMO
    
    n_electrons = Wavefunction.nalpha()
    
    # Get the orbital coefficients of the HOMO and the LUMO
    if orbs == []:
        Ca = Wavefunction.Ca_subset("AO","ALL").np.T[n_electrons - 1 : n_electrons + 1 ]
    else:
        Ca1 = Wavefunction.Ca_subset("AO","ALL").np[:,orbs[0]]
        Ca2 = Wavefunction.Ca_subset("AO","ALL").np[:,orbs[1]]
        Ca = np.vstack(Ca1,Ca2)
    
    # Normalize the vectors containing the orbital coefficients
#    for i in range(0,len(Ca)):
#     Ca[i] = Ca[i]/np.sum(Ca[i]**2)**0.5
    
    dx,dy,dz = dxyz 
    Vele = dx*dy*dz                                 # Volume element    
    x = np.arange(box['xmin'],box['xmax'],dx)                       # Grid points along a single dimension
    y = np.arange(box['ymin'],box['ymax'],dy)                       # Grid points along a single dimension
    z = np.arange(box['zmin'],box['zmax'],dz)                       # Grid points along a single dimension
    X,Y,Z = np.meshgrid(x,x,x)                   # Create a mesh grid contaning the X,Y,Z coordinates
    MOs = np.zeros((len(Ca),len(x),len(y),len(z)))        # Initialize the 4D matrix (Orbital, X,Y,Z)
    
    # Calculate the molecular orbitals
    for i in range(len(x)):
     for j in range(len(y)):
      for k in range(len(z)):
       #MOs[i,j,k] = Vele**0.5*np.dot(Ca,Wavefunction.basisset().compute_phi(X[i,j,k],Y[i,j,k],Z[i,j,k]))
       ao_vals = Wavefunction.basisset().compute_phi(X[i,j,k],Y[i,j,k],Z[i,j,k])
       MOs[:,i,j,k] = Vele**0.5*Ca@ao_vals
    
    # Get the HOMO and LUMO as 3D matrices
    HOMO = MOs[0,:,:,:] 
    LUMO = MOs[1,:,:,:]
    
    # Return these two arrays
    return HOMO, LUMO, dx
    
    
# genOBJs: Generate the .OBJ 3D files that will be read by Blender    
def genOBJs(Initial_State, Final_State, dx, N_frames):
    for t in range(0,N_frames):  
     psi = np.cos(t*np.pi/(2*N_frames)) * Initial_State + np.sin(t*np.pi/(2*N_frames)) * Final_State * np.exp(-1j*t*2*np.pi/25)  
#     psi = Initial_State 
     Psi_squared = abs(psi)**2
     verts, faces, normals, values = measure.marching_cubes(Psi_squared, 0.00001) 
     o = open('tmpOBJs/%s.obj' % t,'w')
     o.write('o Wavefunction\n')
     for i in verts:
      o.write('v %s %s %s \n' %(i[0]*dx-6,i[1]*dx-6,i[2]*dx-6))
     for f in faces:
      i = verts[f[0]]
      a,b,c = map(int,i)
      if psi[a,b,c] > 0:
       o.write('vt %s %s \n' % (0,0))
      else:
       o.write('vt %s %s \n' % (0.5,0))
     c = 1
     for i in faces:
      o.write('f %s/%s %s/%s %s/%s \n' %(i[0]+1,c,i[1]+1,c,i[2]+1,c))
      c+=1
     o.close()



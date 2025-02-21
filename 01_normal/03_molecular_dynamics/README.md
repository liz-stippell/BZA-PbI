# Molecular Dynamics Simulations 

#### Computed using the VASP software package

Here, there are three different simulations ran (in order):

  1. <b> NVT: </b> Heat up the system to the desired temperature.
  2. <b> NVT: </b> Equilibrate the system at the desired temperature.
  3. <b> NVE: </b> Trajectory of the molecular dynamics simulation at the desired length.

Each step has five files needed to run:
- <b> INCAR: </b> The input file
- <b> POSCAR: </b> The starting geometry
    - This is taken from the CONTCAR of the geometry optimization step, renamed to POSCAR for the temperature ramp step
    - The previous MD simulation's CONTCAR is used as the POSCAR for the next MD simulation
- <b> POTCAR: </b> Potential files
- <b> KPOINTS: </b> K-Points mesh for system
- <b> SUB_VASP: </b> Submit script for working with HPC

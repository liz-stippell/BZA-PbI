# BZA-PbI

# The steps for this project, organized in chronological order as follows:

## 1. Geometry Optimization (VASP)
#### Computed using the VASP software package
#### Files:
- <b> INCAR </b>
- <b> POSCAR </b>
- <b> POTCAR </b>
- <b> KPOINTS </b>
- <b> SUB_VASP </b>
- <b> PbI6BZA.vasp </b>

## 2. Static Calculation (VASP)
- For computing the projected density of states (pDOS) of the system.
#### Computed using the VASP software package
#### Files:
- <b> INCAR </b>
- <b> POSCAR </b>
- <b> POTCAR </b>
- <b> KPOINTS </b>
- <b> SUB_VASP </b>

This step utilizes the optimized geometry from the first step (Geometry Optimization)

## 3. Molecular Dynamics Simulation (VASP)
  1. <b> NVT: </b> Heat up the system to the desired temperature.
  2. <b> NVT: </b> Equilibrate the system at the desired temperature.
  3. <b> NVE: </b> Trajectory of the molecular dynamics simulation at the desired length.

## 4. Single Point Calculations (OpenMX)
- For computing the electronic coupling of the system.

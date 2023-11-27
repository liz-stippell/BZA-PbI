#!/bin/bash
#SBATCH --job-name=Python
#SBATCH --account=prezhdo_176
###SBATCH --partition=epyc-64
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=out.log
#SBATCH --error=out.err
#SBATCH --mem=0

#SBATCH --mail-user=stippell@usc.edu
#SBATCH --mail-type=ALL


module purge
module load intel/19.0.4
module load intel-mpi/2019.4.243
module load intel-mkl/2019.5.281
module load gcc/11.3.0
#module load python/3.7.6
module load python/3.9.12
export PYTHONPATH=$PYTHONPATH:$PWD
#export PYTHONPATH=$PYTHONPATH:/project/prezhdo_176/morapere/morapere/code/python_pkgs
export PYTHONPATH=$PYTHONPATH:/project/prezhdo_176/morapere/morapere/code/ase

export PYTHONPATH=$PYTHONPATH:/home1/stippell/Conda/Miniconda3/lib/python3.9/site-packages #/TB2J_OpenMX-0.4.2-py3.9-linux-x86_64.egg/TB2J_OpenMX


python plot_ecoupling.py

#python run-e-coupling.py

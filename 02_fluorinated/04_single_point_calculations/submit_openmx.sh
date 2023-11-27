#!/bin/bash
#SBATCH --job-name=openmx_NORMAL
#SBATCH --account=prezhdo_176
###SBATCH --partition=prezhdo
###SBATCH --partition=main
#SBATCH --partition=oneweek
#SBATCH --nodes=2
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00
#SBATCH --output=out-%A_%a.log
#SBATCH --error=out-%A_%a.err
#SBATCH --mem=0

#SBATCH --mail-user=stippell@usc.edu
#SBATCH --mail-type=ALL


cd $SLURM_SUBMIT_DIR

module purge
module load intel/19.0.4
module load openmx
module load intel-oneapi
#module load intel-mpi/2019.4.243
#module load intel-mkl/2019.5.281

ulimit -s unlimited

#mpirun -np 2 openmx openmx_in.dat > openmx.std


MINT=2809
MAXT=3000

for i in `seq $MINT $MAXT`
do
    t=$((i))
    printf "calculate  at t = $t fs  \n"
    rm -rf $i
    mkdir $i
    SUFX=$( printf "%d" "$t" )

    POSFILE="PbI.${SUFX}.dat"
    cp wd/$POSFILE $i/
    cd $i
    mpirun -n 2 openmx $POSFILE > out
#    srun  openmx $POSFILE > out
    rm out *.cube *.grid *md* *xyz *scf *ene
    rm -rf c4_rst
    cd ..
done

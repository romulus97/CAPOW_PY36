#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH --mem-per-cpu=3000
#SBATCH -n $
#SBATCH -t $-00:00:00
#SBATCH --array=38-199


cd LR/CA$SLURM_ARRAY_TASK_ID
python CA_simulation.py $SLURM_ARRAY_TASK_ID

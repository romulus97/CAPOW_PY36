#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH --mem-per-cpu=3000
#SBATCH -n 8
#SBATCH -t 2-00:00:00
#SBATCH --array=1-50


cd CAISO_$SLURM_ARRAY_TASK_ID
python3 simulation.py $SLURM_ARRAY_TASK_ID

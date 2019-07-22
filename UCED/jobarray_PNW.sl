#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH --mem-per-cpu=3000
#SBATCH -n 4
#SBATCH -t 4-00:00:00
#SBATCH --array=38-199


cd LR/PNW$SLURM_ARRAY_TASK_ID
python PNW_simulation.py $SLURM_ARRAY_TASK_ID

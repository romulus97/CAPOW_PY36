#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH --mem-per-cpu=2000
#SBATCH -n 8
#SBATCH -t 2-00:00:00
#SBATCH --array=1-50


cd PNW_$SLURM_ARRAY_TASK_ID
python3 PNW_simulation.py $SLURM_ARRAY_TASK_ID

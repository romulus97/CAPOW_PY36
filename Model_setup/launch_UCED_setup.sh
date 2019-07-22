#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 01-00:00:00
#SBATCH --mem=16g
#SBATCH -n 8
#SBATCH --array=1-10

python3 UCED_setup_LR$SLURM_ARRAY_TASK_ID.py

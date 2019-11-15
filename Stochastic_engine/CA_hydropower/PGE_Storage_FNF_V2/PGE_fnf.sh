#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 07-00:00:00
#SBATCH --mem=16g
#SBATCH -n 5


python FNF_DE_regular_dams_PGE.py

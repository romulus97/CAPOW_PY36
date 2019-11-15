#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 03-00:00:00
#SBATCH --mem=16g
#SBATCH -n 5


python rule_based_flexible_de_run_1_SCE.py

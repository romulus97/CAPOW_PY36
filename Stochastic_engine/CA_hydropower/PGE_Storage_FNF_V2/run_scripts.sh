#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 03-00:00:00
#SBATCH --mem=32g
#SBATCH -n 5


python run_scripts.py
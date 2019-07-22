#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 00-00:10:00
#SBATCH --mem=1g
#SBATCH -n 1

python3 hourly_prices_merge.py

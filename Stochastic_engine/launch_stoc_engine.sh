#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -t 00-24:00:00
#SBATCH --mem=2g
#SBATCH -n 8


python3 stochastic_engine.py

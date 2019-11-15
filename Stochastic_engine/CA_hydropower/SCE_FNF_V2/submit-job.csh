#!/bin/tcsh

# Set up python and cplex environment
module load python3
source /share/infews/jkern/my_venv/bin/activate.csh
source /usr/local/apps/cplex/cplex.csh

bsub -q cnr -W 5000 -o out.%J -e err.%J "python rule_based_flexible_de_run_1_SCE.py"



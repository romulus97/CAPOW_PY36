#!/bin/tcsh

# Set up python and cplex environment
module load python3
source /share/infews/jkern/my_venv/bin/activate.csh
source /usr/local/apps/cplex/cplex.csh

bsub -q cnr -W 5760 -o out.%J -e err.%J "python FNF_DE_regular_dams_PGE.py"



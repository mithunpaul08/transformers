#!/usr/bin/env bash
export DATA_DIR_BASE="../src/transformers/data/datasets"
export DATASET="fever"
export basedir="$DATA_DIR_BASE/$DATASET"
export TASK_TYPE="lex" #options for task type include lex,delex,and combined"". combined is used in case of student teacher architecture which will load a paralleldataset from both lex and delex folders
export SUB_TASK_TYPE="figerspecific" #options for TASK_SUB_TYPE (usually used only for delex)  include [oa, figerspecific, figerabstract, oass, simplener]
export TASK_NAME="fevercrossdomain" #options for TASK_NAME  include fevercrossdomain,feverindomain,fnccrossdomain,fncindomain
export DATA_DIR="$DATA_DIR_BASE/$DATASET/$TASK_NAME/$TASK_TYPE/$SUB_TASK_TYPE"
#export PYTHONPATH="/Users/mordor/research/transformers/src"

#comment this section if you just downloaded and converted the data fresh using these.-useful for repeated runs
rm -rf $basedir
./get_fever_fnc_data.sh
./reduce_size.sh
./convert_to_mnli_format.sh
#############end of commentable data sections
./run_glue.sh


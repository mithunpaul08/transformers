#!/usr/bin/env bash

#make sure ./get_fever_fnc_data.sh is run before this file

#cd /home/u11/mithunpaul/huggingfacev2/mithun_scripts/
#relative paths that worked on june 6th


echo "value of epochs in runglue.sh is $EPOCHS"

echo "TASK_TYPE is $TASK_TYPE"
if [ "$TASK_TYPE" = "delex" ] ; then
 echo $DATA_DIR
 echo "task type is delex"

fi

echo "TASK_TYPE is $TASK_TYPE"
if [ "$TASK_TYPE" = "lex" ] ; then
 echo $DATA_DIR
 echo "task type is lex"
fi

if [ "$TASK_TYPE" = "combined" ] ; then
 echo $DATA_DIR
 echo "task type is combined"
 args="$args --do_train_1student_1teacher"
fi

echo "data_dir is $DATA_DIR"


echo $args

mkdir -p OUTPUT_DIR

env CUDA_VISIBLE_DEVICES=0
export CUDA_VISIBLE_DEVICES=0
if [ $MACHINE_TO_RUN_ON == "hpc" ]; then
       python3.6 ../examples/text-classification/run_glue.py $args
else
       python3 ../examples/text-classification/run_glue.py $args
fi



### how to run 

`mkdir factverfication`

`cd factverification`

`mkdir code`

`mkdir output`

`mkdir data`

`cd code`

`git clone git@github.com:mithunpaul08/transformers.git .`

`cd mithun_scripts`


change the paths in the following code to the corresponding ones.
also pick a name you want to run on as $MACHINE_TO_RUN_ON

```
if [ $MACHINE_TO_RUN_ON == "clara" ]; then
        wandb on
        wandb online
        export OUTPUT_DIR_BASE="/work/mithunpaul/huggingface_bertmini_multiple_teachers_v1/output"
        export DATA_DIR_BASE="/work/mithunpaul/huggingface_bertmini_multiple_teachers_v1/data"
fi

```

also change the paramaters of below values

```
export DATASET="fever" #options include [fever, fnc]
export TASK_TYPE="3t1s" #options for task type include lex,delex,and combined"". combined is used in case of student teacher architecture which will load a paralleldataset from both mod1 and mod2 folders
export SUBTASK_TYPE="few_shot"
export TASK_NAME="fevercrossdomain" #options for TASK_NAME  include fevercrossdomain,feverindomain,fnccrossdomain,fncindomain
export BERT_MODEL_NAME="google/bert_uncased_L-12_H-128_A-2" #options include things like [bert-base-uncased,bert-base-cased] etc. refer src/transformers/tokenization_bert.py for more.
export MAX_SEQ_LENGTH="128"
```

then run the code using:

`bash run_all.sh --epochs_to_run 25 --machine_to_run_on hpc --use_toy_data false --download_fresh_data true `

note: change the $MACHINE_TO_RUN_ON to whatever you picked above
# Command Line Arguments
command line args to change in ./run_all.sh:

### to train just 1 model (lex or delex)


- remove  `--do_train_student_teacher`
- total_no_of_models_including_student_and_its_teachers=1
- total_no_of_test_datasets=1
- task_type=[lex or delex]

e.g.,`--total_no_of_models_including_student_and_its_teachers 1 --total_no_of_test_datasets 1 --task_type lex`

## to run 2 models (as student teacher architecture)
pass command line args:
total_no_of_models_including_student_and_its_teachers=2
total_no_of_test_datasets=2
TASK_TYPE=combined


e.g.,
`--task_type combined --do_train_student_teacher  --total_no_of_models_including_student_and_its_teachers 2 --total_no_of_test_datasets 2`


## to run 4 models (as  group learning architecture)
pass command line args:

- --do_train_student_teacher
- total_no_of_models_including_student_and_its_teachers=4 

- total_no_of_test_datasets=4

- TASK_TYPE=3t1s


e.g.,
`--task_type 3t1s --do_train_student_teacher  --total_no_of_models_including_student_and_its_teachers 4 --total_no_of_test_datasets 4`

order of 4 models : 

- model1=lex
- model2=figerspecific
- model3=oaner
- model4=figerabstract

## Few Shot Learning with Group Learning
- go to get_fever_fnc_data.sh and check if you have the right number of data points from cross domain
under your condition. 
e.g.,look under
`if [ "$TASK_TYPE" = "lex" ] && [ "$TASK_NAME" = "fevercrossdomain" ] && [ "$SUBTASK_TYPE" = "few_shot" ];`



## other command line arguments

`--overwrite_cache` : add this if you want the cache to be overwritten. Usually the 
tokenized data is stored and reused from the cache. Especially when `--download_fresh_data` is set
to True, it is imperative that `--overwrite_cache` is added to the list of arguments.

`--machine_to_run_on clara`: this is just the name of our machine here. You can use whatever machine you want. More important part is you need to change
go to ./run_all.sh and under `--machine_to_run_on` export the paths for `OUTPUT_DIR_BASE` `DATA_DIR_BASE`, which 
are the absolute paths to outputdirectory and the data directory you created earlier.


`--use_toy_data false` : you can set this to True if you want to try on a very small sixe of data 
 --download_fresh_data true`

`--classification_loss_weight`: how much weight you want to assign for classification loss as oppoosed to consistency loss (
whose default weight is 1.). refer paper for details. used during training/tuning only

## Typical examples of command line arguments. 

- to run a stand alone model which trains on lexicalized plain text data. This is the classic training of any neural network. 

```
--model_name_or_path google/bert_uncased_L-12_H-128_A-2 --task_name fevercrossdomain --do_train --do_eval --do_predict --data_dir /Users/mordor/research/huggingface/src/transformers/data/datasets/fever/fevercrossdomain/lex/toydata/ --max_seq_length 128 --per_device_eval_batch_size=16 --per_device_train_batch_size=16 --learning_rate 1e-5 --num_train_epochs 2 --output_dir /Users/mordor/research/huggingface/mithun_scripts/output/fever/fevercrossdomain/lex/google/bert_uncased_L-12_H-128_A-2/128/ --overwrite_output_dir --weight_decay 0.01 --adam_epsilon 1e-6 --evaluate_during_training --task_type lex --machine_to_run_on laptop --toy_data_dir_path /Users/mordor/research/huggingface/src/transformers/data/datasets/fever/fevercrossdomain/lex/toydata/ --overwrite_cache --total_no_of_models_including_student_and_its_teachers 1 --total_no_of_test_datasets 1

```

# To start training

go to ./run_all.sh
- under --machine_to_run_onexport the paths for `OUTPUT_DIR_BASE` `DATA_DIR_BASE`, which 
are the absolute paths to outputdirectory and the data directory you created earlier.
e.g.,`export OUTPUT_DIR_BASE="/work/mithunpaul/huggingface_bertmini_multiple_teachers_v1/output"`

Then run this command in ./mithun_scripts. 

`bash run_all.sh --epochs_to_run 55 --machine_to_run_on clara --use_toy_data false --download_fresh_data true`

  
# for Internal reference:

to run on hpc:

- make sure that this line is the last line in ./run_on_hpc_ocelote_venv_array.sh
`bash run_all.sh --epochs_to_run 25 --machine_to_run_on hpc --use_toy_data false --download_fresh_data true #options include [laptop, hpc,clara]`

- login to hpc (short cut keyh, followed by key o)
- cd to right folder+ copy folder path

- go to ./run_on_hpc_ocelote_venv_array.sh change absolute path to folder path at 3 locations
export PYTHONPATH="/home/u11/mithunpaul/xdisk/lexStandAlone_fever2fnc/code/src"

- go to ./run_all.sh, change the folderpath at 2 locations

- qsub run_on_hpc_ocelote_venv_array.sh 

`bash run_all.sh --epochs_to_run 2 --machine_to_run_on laptop --use_toy_data true --download_fresh_data true`


`bash run_all.sh --epochs_to_run 25 --machine_to_run_on clara --use_toy_data false --download_fresh_data true`
[BERT]
model_name_or_path="bert-base-cased"
task_name="fevercrossdomain"
do_train=True
do_eval=True
do_predict=True
#do_train_1student_1teacher=True
data_dir="/home/u11/mithunpaul/xdisk/huggingface_bert_fever_to_fnc_attention_weights_branch/data/fever/fevercrossdomain/lex/figerspecific/"
max_seq_length="128"
per_device_eval_batch_size="16"
per_device_train_batch_size="16"
learning_rate="1e-5"
# Note: use num_train_epochs=1 only. For testing purposes, in trainery.py we are as of now, sep 2020 we are returning the dev and test partition evaluation results for epoch1
# if you want to test for more than 1 eopch, return best_dev and best_test values
num_train_epochs="1"
output_dir="/home/u11/mithunpaul/xdisk/huggingface_bert_fever_to_fnc_attention_weights_branch/output/fever/fevercrossdomain/lex/figerspecific/bert-base-cased/128/"
overwrite_output_dir=True
weight_decay="0.01"
adam_epsilon="1e-6"
evaluate_during_training=True
task_type="lex"
subtask_type="figerspecific"
machine_to_run_on="hpc"
toy_data_dir_path="/Users/mordor/research/huggingface/src/transformers/data/datasets/fever/fevercrossdomain/lex/figerspecific/toydata/"
#what are the scores that you should assert against. i.e the ones we got when we ran the toy data alone
fever_in_domain_accuracy_on_toy_data_17_datapoints=0.9375
fever_cross_domain_accuracy_on_toy_data_17_datapoints=0.875
fever_cross_domain_fncscore_on_toy_data_17_datapoints=0.9
overwrite_cache=True
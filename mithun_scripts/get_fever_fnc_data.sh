#!/bin/bash


export BASE_DATA_DIR="../src/transformers/data/datasets/"

cd $BASE_DATA_DIR
#comment this folder removal only if you are sure that the data you have is in fever tsv format. else its better to remove and download data fresh.
rm -rf fever

#pick according to which kind of dataset you want to use for  train, dev, test on. Eg: train on fever, test on fnc

#######indomain fever

mkdir -p fever/feverindomain/lex


FILE=fever/feverindomain/lex/train.tsv
if test -f "$FILE";then
    echo "$FILE exists"
else
    wget https://storage.googleapis.com/fact_verification_mithun_files/TSV/FEVER/in-domain/lex/train.tsv -O $FILE
fi

FILE=fever/feverindomain/lex/dev.tsv
if test -f "$FILE";then
    echo "$FILE exists"
else
    wget https://storage.googleapis.com/fact_verification_mithun_files/TSV/FEVER/in-domain/lex/dev.tsv -O $FILE
fi
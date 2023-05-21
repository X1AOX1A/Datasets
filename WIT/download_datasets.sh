#!/bin/bash

# Download and merge the training set
echo "Downloading and merging the training set..."
for i in {0..9}
do
    echo "Downloading wit_v1.train.all-0000${i}-of-00010.tsv.gz..."
    wget "https://storage.googleapis.com/gresearch/wit/wit_v1.train.all-0000${i}-of-00010.tsv.gz"
    gunzip wit_v1.train.all-0000${i}-of-00010.tsv.gz
    cat wit_v1.train.all-0000${i}-of-00010.tsv >> train.tsv
    rm wit_v1.train.all-0000${i}-of-00010.tsv
done

# Download and merge the validation set
echo "Downloading and merging the validation set..."
for i in {0..4}
do
    echo "Downloading wit_v1.val.all-0000${i}-of-00005.tsv.gz..."
    wget "https://storage.googleapis.com/gresearch/wit/wit_v1.val.all-0000${i}-of-00005.tsv.gz"
    gunzip wit_v1.val.all-0000${i}-of-00005.tsv.gz
    cat wit_v1.val.all-0000${i}-of-00005.tsv >> valid.tsv
    rm wit_v1.val.all-0000${i}-of-00005.tsv
done

# Download and merge the test set
echo "Downloading and merging the test set..."
for i in {0..4}
do
    echo "Downloading wit_v1.test.all-0000${i}-of-00005.tsv.gz..."
    wget "https://storage.googleapis.com/gresearch/wit/wit_v1.test.all-0000${i}-of-00005.tsv.gz"
    gunzip wit_v1.test.all-0000${i}-of-00005.tsv.gz
    cat wit_v1.test.all-0000${i}-of-00005.tsv >> test.tsv
    rm wit_v1.test.all-0000${i}-of-00005.tsv
done

echo "Download and merge complete."
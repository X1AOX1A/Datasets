#!/bin/bash

# Create directories
mkdir "train"
mkdir "valid"
mkdir "test"

# Download training set
for i in {0..4}; do
    wget -P "train" "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-train.tfrecord.gz-0000${i}-of-00005"
done

# Download validation set
wget -P "valid" "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-val.tfrecord.gz"

# Download test set
wget -P "test" "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-test.tfrecord.gz"
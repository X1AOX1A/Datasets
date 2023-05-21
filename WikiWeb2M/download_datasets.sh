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

# Extract compressed files
cat wikiweb2m-train.tfrecord.gz-000* > wikiweb2m-train.tfrecord.gz
rm wikiweb2m-train.tfrecord.gz-000*
gzip -d "wikiweb2m-train.tfrecord.gz"
gzip -d "wikiweb2m-val.tfrecord.gz"
gzip -d "wikiweb2m-test.tfrecord.gz"

# Create index files
# pip3 install tfrecord
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-train.tfrecord wikiweb2m-train.tfidnex
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-val.tfrecord wikiweb2m-val.tfidnex
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-test.tfrecord wikiweb2m-test.tfidnex
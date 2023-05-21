#!/bin/bash

## Download datasets
echo "Downloading datasets..."
for i in {0..4}; do
    echo "Downloading wikiweb2m-train.tfrecord.gz-0000${i}-of-00005"
    wget "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-train.tfrecord.gz-0000${i}-of-00005"
done
echo "Downloading wikiweb2m-val.tfrecord.gz"
wget "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-val.tfrecord.gz"
echo "Downloading wikiweb2m-test.tfrecord.gz"
wget "https://storage.googleapis.com/gresearch/wit/wikiweb2m/wikiweb2m-test.tfrecord.gz"

## Extract compressed files
echo "Extracting compressed files..."
echo "Combining wikiweb2m-train.tfrecord.gz parts into a single file"
cat wikiweb2m-train.tfrecord.gz-000* > wikiweb2m-train.tfrecord.gz
rm wikiweb2m-train.tfrecord.gz-000*
echo "Decompressing wikiweb2m-train.tfrecord.gz"
gzip -d "wikiweb2m-train.tfrecord.gz"
echo "Decompressing wikiweb2m-val.tfrecord.gz"
gzip -d "wikiweb2m-val.tfrecord.gz"
echo "Decompressing wikiweb2m-test.tfrecord.gz"
gzip -d "wikiweb2m-test.tfrecord.gz"

## Create index files
# pip3 install tfrecord
echo "Creating index files..."
echo "Creating index for wikiweb2m-train.tfrecord"
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-train.tfrecord wikiweb2m-train.tfidnex
echo "Creating index for wikiweb2m-val.tfrecord"
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-val.tfrecord wikiweb2m-val.tfidnex
echo "Creating index for wikiweb2m-test.tfrecord"
python3 -m tfrecord.tools.tfrecord2idx wikiweb2m-test.tfrecord wikiweb2m-test.tfidnex
echo "Done!"
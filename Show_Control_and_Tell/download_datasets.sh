#!/bin/bash

# COCO Entities
echo "Downloading COCO Entities annotations and metadata..."
wget -O dataset_coco.tgz https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/dataset_coco.tgz
echo "Extracting dataset_coco.tgz..."
tar -xzvf dataset_coco.tgz

echo "Downloading COCO Entities pre-computed features..."
mkdir -p datasets/coco
wget -O datasets/coco/coco_detections.hdf5 https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/coco_detections.hdf5

# Flickr30k Entities
echo "Downloading Flickr30k Entities annotations and metadata..."
wget -O dataset_flickr.tgz https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/dataset_flickr.tgz
echo "Extracting dataset_flickr.tgz..."
tar -xzvf dataset_flickr.tgz

echo "Downloading Flickr30k Entities pre-computed features..."
mkdir -p datasets/flickr
wget -O datasets/flickr/flickr30k_detections.hdf5 https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/flickr30k_detections.hdf5

echo "Download and extraction complete."
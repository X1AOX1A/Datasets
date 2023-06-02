#!/bin/bash

# Create the target directories
mkdir -p "download"
mkdir -p "images"
mkdir -p "annotations"

# Loop through each link
declare -A links=(
    ['train']='http://images.cocodataset.org/zips/train2014.zip'
    ['val']='http://images.cocodataset.org/zips/val2014.zip'
    ['test']='http://images.cocodataset.org/zips/test2014.zip'
    ['test2015']='http://images.cocodataset.org/zips/test2015.zip'
)

for key in "${!links[@]}"; do
    link="${links[$key]}"
    
    # Download the file
    echo "Downloading $key..."
    wget -P $download_dir $link
    
    # Extract the file
    echo "Extracting $key..."
    unzip -q "$download_dir/$key" -d $unzip_dir
    
    # Remove the downloaded zip file
    # rm "$download_dir/$key"
done

# Download the annotations
echo "Downloading annotations..."
urls=(
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_train.json"
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_val.json"
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_test.json"
)

for url in "${urls[@]}"
do
  wget "$url" -P "annotations/"
done

echo "Download and extraction completed!"
#!/bin/bash

# Define the target directories
download_dir="download"
unzip_dir="images"

# Create the target directories
mkdir -p $download_dir
mkdir -p $unzip_dir

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
    unzip -q "$download_dir/$(basename $link)" -d $unzip_dir
    
    # Remove the downloaded zip file
    # rm "$download_dir/$(basename $link)"
done

echo "Download and extraction completed!"
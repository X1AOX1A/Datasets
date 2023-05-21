#!/bin/bash

# Create directories
echo "Creating directories..."
mkdir "Open_Image"
mkdir "COCO"
mkdir "Flickr30k"
mkdir "ADE20k"

# Download Open Images
echo "Downloading Open Images..."
mkdir "Open_Image/train"
for i in {0..9}; do
    echo "Downloading file open_images_train_v6_localized_narratives-0000${i}-of-00010.jsonl"
    wget -P "Open_Image/train" "https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-0000${i}-of-00010.jsonl"
done
echo "Merging Open Images JSONL files..."
cat Open_Image/train/*.jsonl > Open_Image/train.jsonl
rm -rf Open_Image/train
wget -P "Open_Image" "https://storage.googleapis.com/localized-narratives/annotations/open_images_validation_localized_narratives.jsonl"
wget -P "Open_Image" "https://storage.googleapis.com/localized-narratives/annotations/open_images_test_localized_narratives.jsonl"

# Download COCO
echo "Downloading COCO..."
mkdir "COCO/train"
for i in {0..3}; do
    echo "Downloading file coco_train_localized_narratives-0000${i}-of-00004.jsonl"
    wget -P "COCO/train" "https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-0000${i}-of-00004.jsonl"
done
echo "Merging COCO JSONL files..."
cat COCO/train/*.jsonl > COCO/train.jsonl
rm -rf COCO/train
wget -P "COCO" "https://storage.googleapis.com/localized-narratives/annotations/coco_val_localized_narratives.jsonl"

# Download Flickr30k
echo "Downloading Flickr30k..."
wget -P "Flickr30k" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_train_localized_narratives.jsonl"
wget -P "Flickr30k" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_val_localized_narratives.jsonl"
wget -P "Flickr30k" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_test_localized_narratives.jsonl"

# Download ADE20k
echo "Downloading ADE20k..."
wget -P "ADE20k" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_train_localized_narratives.jsonl"
wget -P "ADE20k" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_validation_localized_narratives.jsonl"

echo "Download complete."

#!/bin/bash

# Create directories
mkdir "Open Image"
mkdir "COCO"
mkdir "Flickr30k"
mkdir "ADE20k"

# Download Open Images
mkdir "Open Image/train"
for i in {0..9}; do
    wget -P "Open Image/train" "https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-0000${i}-of-00010.jsonl"
done

mkdir "Open Image/valid"
wget -P "Open Image/valid" "https://storage.googleapis.com/localized-narratives/annotations/open_images_validation_localized_narratives.jsonl"

mkdir "Open Image/test"
wget -P "Open Image/test" "https://storage.googleapis.com/localized-narratives/annotations/open_images_test_localized_narratives.jsonl"

# Download COCO
mkdir "COCO/train"
for i in {0..3}; do
    wget -P "COCO/train" "https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-0000${i}-of-00004.jsonl"
done

mkdir "COCO/valid"
wget -P "COCO/valid" "https://storage.googleapis.com/localized-narratives/annotations/coco_val_localized_narratives.jsonl"

# Download Flickr30k
mkdir "Flickr30k/train"
wget -P "Flickr30k/train" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_train_localized_narratives.jsonl"

mkdir "Flickr30k/valid"
wget -P "Flickr30k/valid" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_val_localized_narratives.jsonl"

mkdir "Flickr30k/test"
wget -P "Flickr30k/test" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_test_localized_narratives.jsonl"

# Download ADE20k
mkdir "ADE20k/train"
wget -P "ADE20k/train" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_train_localized_narratives.jsonl"

mkdir "ADE20k/valid"
wget -P "ADE20k/valid" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_validation_localized_narratives.jsonl"
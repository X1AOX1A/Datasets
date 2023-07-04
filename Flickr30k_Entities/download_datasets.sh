#!/bin/bash

echo "Downloading UNRELATED_CAPTIONS..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/UNRELATED_CAPTIONS

echo "Downloading annotations.zip..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/annotations.zip

echo "Unziping annotations.zip..."
unzip annotations.zip

echo "Downloading flickr30k_entities_utils.py..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/flickr30k_entities_utils.py

echo "Downloading getAnnotations.m..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/getAnnotations.m

echo "Downloading getSentenceData.m..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/getSentenceData.m

echo "Downloading test.txt..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/test.txt

echo "Downloading train.txt..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/train.txt

echo "Downloading val.txt..."
wget https://github.com/BryanPlummer/flickr30k_entities/raw/master/val.txt

echo "Download complete."
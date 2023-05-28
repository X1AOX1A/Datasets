# conda create -n lavis python=3.8
# conda activate lavis

# # Install LAVIS from source
# cd ~/Documents/DEMOS
# git clone https://github.com/salesforce/LAVIS.git
# cd LAVIS
# pip install -e .

cd lavis/datasets/download_scripts/
python download_coco.py
mv /root/Documents/CACHE/lavis/coco /root/Documents/DATASETS/MS_COCO
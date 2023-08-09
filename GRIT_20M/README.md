# GRIT-20M

- We introduce GRIT, a large-scale dataset of **Gr**ounded **I**mage-**T**ext pairs, which is created based on image-text pairs from a subset of COYO-700M and LAION-2B.
- We construct a pipeline to extract and link text spans (i.e., noun phrases, and referring expressions) in the caption to their corresponding image regions.
More details can be found in the paper.

## Data Features

```python
{
  'key': '000373938', 
  'clip_similarity_vitb32': 0.353271484375, 
  'clip_similarity_vitl14': 0.2958984375, 
  'id': 1795296605919, 
  'url': "https://www.thestrapsaver.com/wp-content/uploads/customerservice-1.jpg", 
  'caption': 'a wire hanger with a paper cover that reads we heart our customers', 
  'width': 1024, 
  'height': 693, 
  'noun_chunks': [[19, 32, 0.019644069503434333, 0.31054004033406574, 0.9622142865754519, 0.9603442351023356, 0.79298526], [0, 13, 0.019422357885505368, 0.027634161214033764, 0.9593302408854166, 0.969467560450236, 0.67520964]], 
  'ref_exps': [[19, 66, 0.019644069503434333, 0.31054004033406574, 0.9622142865754519, 0.9603442351023356, 0.79298526], [0, 66, 0.019422357885505368, 0.027634161214033764, 0.9593302408854166, 0.969467560450236, 0.67520964]]
}

```
- `key`: The file name in COYO-700M.
- `clip_similarity_vitb32`: The cosine similarity between text and image(ViT-B/32) embeddings by [OpenAI CLIP](https://github.com/openai/CLIP), provided by COYO-700M.
- `clip_similarity_vitl14`: The cosine similarity between text and image(ViT-L/14) embeddings by [OpenAI CLIP](https://github.com/openai/CLIP), provided by COYO-700M.
- `id`: Unique 64-bit integer ID in COYO-700M.
- `url`: The image URL.
- `caption`: The corresponding caption.
- `width`: The width of the image.
- `height`: The height of the image.
- `noun_chunks`: The noun chunks (extracted by [spaCy](https://spacy.io/)) that have associated bounding boxes (predicted by [GLIP](https://github.com/microsoft/GLIP)). The items in the children list respectively represent 'Start of the noun chunk in caption', 'End of the noun chunk in caption', 'normalized x_min', 'normalized y_min', 'normalized x_max', 'normalized y_max', 'confidence score'.
- `ref_exps`: The corresponding referring expressions. If a noun chunk has no expansion, we just copy it. 

## Data Example

- For more real data samples, please ref to this [markdown](./data_samples.md).

```
NA
```

Run the following commands to visualize it:
```bash
python data/visualize_GRIT.py
```

<div style="display: flex; flex-wrap: wrap;">
  <div style="flex: 50%;">
    <img src="../Examples/GRIT_20M/GRIT_0.png" alt="example0" style="width: 100%;">
    <img src="../Examples/GRIT_20M/GRIT_1.png" alt="example1" style="width: 100%;">
  </div>
  <div style="flex: 50%;">
    <img src="../Examples/GRIT_20M/GRIT_2.png" alt="example2" style="width: 100%;">
    <img src="../Examples/GRIT_20M/GRIT_3.png" alt="example3" style="width: 100%;">
  </div>
</div>


## Download Links

- [GRIT-20M](https://conversationhub.blob.core.windows.net/beit-share-public/kosmos-2/data/GRIT_coyo.jsonl?sv=2021-10-04&st=2023-06-08T11%3A16%3A02Z&se=2033-06-09T11%3A16%3A00Z&sr=c&sp=r&sig=N4pfCVmSeq4L4tS8QbrFVsX6f6q844eft8xSuXdxU48%3D): The split contains about 20M grounded image-caption pairs processed from [COYO-700M](https://huggingface.co/datasets/kakaobrain/coyo-700m).

## Download Script

- Run the following commands to download the dataset:
  ```shell
  cd GRIT_20M  
  export GRIT_20M_ANNO_DOWNLOAD_DIR="./download/grit_coyo.jsonl"
  export IMAGE_URL_LIST_FILE = "./download/url_list.csv"
  export GRIT_20M_IMAGES_DOWNLOAD_DIR="./download/images"
  export GRIT_20M_IMAGE_URL_TO_PATH="./download/image_url_to_path.json"

  ## 1. Download GRIT-coyo annotations
  chmod +x download_datasets.sh
  nohup bash download_datasets.sh $GRIT_20M_ANNO_DOWNLOAD_DIR >nohup.out& 2>&1
  watch -n 1 tail nohup.out
  # You should get 20,508,818 lines in `grit_coyo.jsonl` after downloading.

  ## 2. Download GRIT-coyo images with img2dataset
  # 2.1 install img2dataset
  pip install img2dataset
  
  # 2.2 extract image urls and image_id from `grit_coyo.jsonl` into csv
  python extract_image_url.py --jsonl_path $GRIT_20M_ANNO_DOWNLOAD_DIR --url_list_file $IMAGE_URL_LIST_FILE  
  
  # 2.3 download images
  nohup img2dataset --url_list $IMAGE_URL_LIST_FILE \
    --output_folder $GRIT_20M_IMAGES_DOWNLOAD_DIR \
    --input_format "csv" \
    --output_format "files" \
    --caption_col "image_id" \
    --thread_count 64 \
    --resize_mode "no" \
    --disallowed_header_directives '[]' \
    --enable_wandb "True" \
    --incremental "True" \
    --number_sample_per_shard 10000 >nohup.out& 2>&1
  watch -n 1 tail nohup.out
  
  # 2.4 count the number of images downloaded
  find $GRIT_20M_IMAGES_DOWNLOAD_DIR -type f -name "*.jpg" | grep -c '.jpg$'
  # Your should probably get 12,000,000 images at 2023.07.03.
  # Only get 8,112,182 images due to disk space limitation.

  # 2.5 extract image url to path into json
  python extract_image_path.py --image_root $GRIT_20M_IMAGES_DOWNLOAD_DIR --image_url_to_path $GRIT_20M_IMAGE_URL_TO_PATH
  # {key: image_url, value: image_path}
  # Processed 8112181 images.
  # 430748 dumplicate images (url) skipped.
  # Extracted 7681433 image paths.
  # Writing json file to /root/Documents/DATASETS/GRIT_20M/download/image_url_to_path.json...
  ```

## Filter the Dataset with available images

- The downloaded files are structured as follows:

    ```
    GRIT_20M/
        train.file xxG
        valid.file xxM
        test.file xxM
    ```

## Statistics

- #Images: 90,614,680 (20M available now)
- #Objects: 137,349,210
- #Text Spans: 114,978,233
- Avg Expression Length: 4.7

## Reference

- [Github](https://github.com/microsoft/unilm/tree/master/kosmos-2#GRIT-large-scale-training-corpus-of-grounded-image-text-pairs)
- [Paper](https://github.com/microsoft/unilm/tree/master/kosmos-2#GRIT-large-scale-training-corpus-of-grounded-image-text-pairs)
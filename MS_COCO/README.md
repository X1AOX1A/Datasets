# Microsoft COCO Dataset

[Microsoft COCO Captions dataset](https://github.com/tylin/coco-caption) contains over one and a half million captions describing over 330,000 images. For the training and validation images, five independent human generated captions are be provided for each image.


## Data Features

## Data Example

![Samples from the COCO Caption dataset (Image credit: "https://arxiv.org/pdf/1504.00325.pdf").](https://github.com/salesforce/LAVIS/raw/main/dataset_card/imgs/coco_caption.png)(Samples from the COCO Caption dataset. Image credit: "https://arxiv.org/pdf/1504.00325.pdf")

```python
import json
def read_json(file):
    with open(file, "r") as fp:
        data = json.load(fp)
    return data

ann_paths = {
        "train": 'path/to/coco/annotations/coco_karpathy_train.json',
        "val": 'path/to/coco/annotations/coco_karpathy_val.json',
        "test": 'path/to/coco/annotations/coco_karpathy_test.json',
}

train = read_json(ann_paths["train"])
val = read_json(ann_paths["val"])
test = read_json(ann_paths["test"])

print("Train:\n", train[0])
# Train:
# {
#     'caption': 'A woman wearing a net on her head cutting a cake. ', 
#     'image': 'val2014/COCO_val2014_000000522418.jpg', 
#     'image_id': 'coco_522418'
# }

print("Val:\n"val[0])
# Val:
# {
#     'image': 'val2014/COCO_val2014_000000184613.jpg', 
#     'caption': [
#         'A child holding a flowered umbrella and petting a yak.', 
#         'A young man holding an umbrella next to a herd of cattle.', 
#         'a young boy barefoot holding an umbrella touching the horn of a cow', 
#         'A young boy with an umbrella who is touching the horn of a cow.', 
#         'A boy holding an umbrella while standing next to livestock.'
#     ]
# }

print("Test:\n": test[0])
# Test:
# {
#     'image': 'val2014/COCO_val2014_000000391895.jpg', 
#     'caption': [
#         'A man with a red helmet on a small moped on a dirt road. ', 
#         'Man riding a motor bike on a dirt road on the countryside.', 
#         'A man riding on the back of a motorcycle.', 
#         'A dirt path with a young person on a motor bike rests to the foreground of a verdant area with a bridge and a background of cloud-wreathed mountains. ', 
#         'A man in a red shirt and a red hat is on a motorcycle on a hill side.'
#     ]
# }
```

## Download Links

```python
data_url = {
    "train": "http://images.cocodataset.org/zips/train2014.zip",  # md5: 0da8c0bd3d6becc4dcb32757491aca88
    "val": "http://images.cocodataset.org/zips/val2014.zip",  # md5: a3d79f5ed8d289b7a7554ce06a5782b3
    "test": "http://images.cocodataset.org/zips/test2014.zip",  # md5: 04127eef689ceac55e3a572c2c92f264
    "test2015": "http://images.cocodataset.org/zips/test2015.zip",  # md5: 04127eef689ceac55e3a572c2c92f264
}

annotations = {
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_train.json",
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_val.json",
  "https://storage.googleapis.com/sfr-vision-language-research/datasets/coco_karpathy_test.json",
}
```
- Ref: [lavis/datasets/download_scripts/download_coco.py](https://github.com/salesforce/LAVIS/blob/main/lavis/datasets/download_scripts/download_coco.py)

## Download Script

```shell
cd MS_COCO
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
watch -n 1 tail nohup.out
```

- The downloaded files are structured as follows:

```
MS_COCO/
|-- [ 115]  annotations
|   |-- [1.7M]  coco_karpathy_test.json
|   |-- [ 81M]  coco_karpathy_train.json
|   `-- [1.7M]  coco_karpathy_val.json
|-- [  86]  download
|   |-- [6.2G]  test2014.zip
|   |-- [ 12G]  test2015.zip
|   |-- [ 13G]  train2014.zip
|   `-- [6.2G]  val2014.zip
`-- [  90]  images
    |-- [2.3M]  test
    |-- [6.6M]  test2015
    |-- [6.8M]  train
    `-- [2.4M]  val
```

## Statistics

NA

## Reference

- [Ref](https://github.com/salesforce/LAVIS/blob/main/dataset_card/coco_caption.md)
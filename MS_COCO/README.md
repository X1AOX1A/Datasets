# Microsoft COCO Dataset

[Microsoft COCO Captions dataset](https://github.com/tylin/coco-caption) contains over one and a half million captions describing over 330,000 images. For the training and validation images, five independent human generated captions are be provided for each image.


## Data Features

## Data Example

![Samples from the COCO Caption dataset (Image credit: "https://arxiv.org/pdf/1504.00325.pdf").](https://github.com/salesforce/LAVIS/raw/main/dataset_card/imgs/coco_caption.png)(Samples from the COCO Caption dataset. Image credit: "https://arxiv.org/pdf/1504.00325.pdf")

```python
from lavis.datasets.builders import load_dataset
coco_dataset = load_dataset("coco_caption", vis_path=YOUR_LOCAL_PATH)

print(coco_dataset.keys())
# dict_keys(['train', 'val', 'test'])

print(len(coco_dataset["train"]))
# 566747

print(coco_dataset["train"][0])
# {'image': <PIL.Image.Image image mode=RGB size=640x480>,
#  'text_input': 'A woman wearing a net on her head cutting a cake. ',
#  'image_id': 0}
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
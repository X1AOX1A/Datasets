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

- Download with `lavis`
- Ref: [LAVIS](https://opensource.salesforce.com/LAVIS//latest/getting_started.html#auto-downloading-and-loading-datasets)

## Download Script

```shell
cd DATASET_NAME
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
watch -n 1 tail nohup.out
```

- The downloaded files are structured as follows:

```
DATASET_NAME/
    train.file xxG
    valid.file xxM
    test.file xxM
```

## Statistics

NA

## Reference

- [Ref](https://github.com/salesforce/LAVIS/blob/main/dataset_card/coco_caption.md)
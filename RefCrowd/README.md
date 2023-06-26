# RefCrowd

## Data Features

![example](https://ivipclab.github.io/publication_refcrowd/refcrowd/featured_huf60a27559868fd062be844f5da6460c8_111334_720x2500_fit_q75_h2_lanczos.webp)

RefCrowd is a new challenging referring comprehension dataset for complex real-world crowd grounding, which towards looking for the target person in crowd with referring expressions. Our dataset contains a crowd of persons some of whom share similar visual appearance, and diverse natural languages covering unique properties of the target person. It not only requires to sufficiently mine and understand natural language information, but also requires to carefully focus on subtle diﬀerences between persons in an image, so as to realize fine-grained mapping from language to vision.

In RefCrowd dataset, each image may contains multiple persons, and each person can be described by multiple expressions/sentences. The person location can be denoted as (x_c, y_c, w, h), where (x_c, y_c) denotes the center coordinates of a person, w and h denote its width and height.

The dataset annotations are provided in JSON format. Researchers can read the annotation files by the following Python 3 code:

```python
import json
info_dict=json.load(open(ann_file,'r'))
Images=info_dict['Imgs']    # image annotations
Anns=info_dict['Anns']      # person localization annotations
Refs=info_dict['Refs']      # all expressions for each person annotations
Sents=info_dict['Sents']    # each experssion annotations
Cats=info_dict['Cats']      # only include the person catgory
att_to_ix=info_dict['att_to_ix']    # all attribute categories
att_to_cnt=info_dict['att_to_cnt']  # the number of each attribution in RefCrowd
```

## Data Example

```python
import json

class RefCrowd:
    def __init__(self, ann_file):
        info_dict=json.load(open(ann_file,'r'))
        self.Images=info_dict['Imgs'] # image annotations
        self.Anns=info_dict['Anns'] # person localization annotations
        self.Refs=info_dict['Refs'] # all expressions for each person annotations
        self.Sents=info_dict['Sents'] # each experssion annotations
        self.Cats=info_dict['Cats'] # only include the person catgory
        self.att_to_ix=info_dict['att_to_ix'] # all attribute categories
        self.att_to_cnt=info_dict['att_to_cnt'] # the number of each attribution in RefCrowd

    def get_ann_with_image_id(self, image_id):
        ann = self.Images[image_id]
        sent_ids = ann['sent_ids']
        sent = []
        for sent_id in sent_ids:
            sent.append({
                "sent_id": sent_id,
                "sentence": self.Sents[sent_id]['sentence'],
                "region_id": self.Sents[sent_id]['region_id'],
                "region": self.Sents[sent_id]['region'],
            })
        ann["sentences"] = sent
        return ann

if __name__ == "__main__":
    ann_file = "path/to/RefCrowd/annotations/test.json"
    refcrowd = RefCrowd(ann_file)
    ann = refcrowd.get_ann_with_image_id("00000000")
    print(ann)
```
![example-0](https://camo.githubusercontent.com/2a2c1f81f52901902a0f8c29d6e8d1110de7fd630b9f0b88c482d554dbc69367/68747470733a2f2f7831612d616c696f73732e6f73732d636e2d7368656e7a68656e2e616c6979756e63732e636f6d2f536e6970706574734c61622f3230323330363234313631303933302e6a7067)
```json
{
    "height": 359,
    "width": 640,
    "file_name": "00000000.jpg",
    "image_id": "00000000",
    "region_ids": ["11915", "11916", "11917"],
    "sent_ids": ["24234", "24235", "24236", "24237", "24238", "24239"],
    "refer_ids": ["11915", "11916", "11917"],
    "sentences": [
        {
            "sent_id": "24234",
            "sentence": "a man in a yellow hooked jacket.",
            "region_id": "11915",
            "region": [419.02, 113.73000000000002, 28.090000000000032, 111.39999999999999]
        },
        {
            "sent_id": "24235",
            "sentence": "a man with hands in her pockets.",
            "region_id": "11915",
            "region": [419.02, 113.73000000000002, 28.090000000000032, 111.39999999999999]
        },
        {
            "sent_id": "24236",
            "sentence": "the second person from the left.",
            "region_id": "11916",
            "region": [396.67, 133.32, 27.04, 81.82]
        },
        {
            "sent_id": "24237",
            "sentence": "a man wearing socks.",
            "region_id": "11916",
            "region": [396.67, 133.32, 27.04, 81.82]
        },
        {
            "sent_id": "24238",
            "sentence": "the first person from the right.",
            "region_id": "11917",
            "region": [491.1700000000001, 173.05, 71.58999999999997, 59.31]
        },
        {
            "sent_id": "24239",
            "sentence": "a man sitting on the ground.",
            "region_id": "11917",
            "region": [491.1700000000001, 173.05, 71.58999999999997, 59.31]
        }
    ]
}
```

## Download Links

To ensure the rational use of RefCrowd dataset, researchers requires to sign RefCrowd Terms of Use as restrictions on access to dataset to privacy protection and use dataset for non-commercial research and/or educational purposes.

If you have recieved access, you can download and extract our RefCrowd Dataset.

## Download Script

- The downloaded files are structured as follows:

```
RefCrowd/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
│  
└── annotations/
    ├── train.json
    ├── val.json
    └── test.json
```

## Evaluation

We calculate the intersection-over-union (IoU) between the predicted bounding box and ground-truth one to measure whether the prediction is correct. A predicted bounding is treated as correct if IoU is higher than desired IoU threshold. Instead of using single IoU threshold 0.5, we adopt the mean accuracy mAcc to measure the localization performance of method which averages the accuracy over IoU thresholds from loose 0.5 to strict 0.95 with interval 0.05 similar to popular COCO metrics. mAcc is a comprehensive indicator for widely real-world applications.

For convenience, researchers can refer to the code ([refcrowd.py](https://github.com/QiuHeqian/MMDetection-REF)) provided by us for reading annotations and evaluation method.

If you have any question, please concat us (hqqiu@std.uestc.edu.cn).

## Statistics

This dataset contains 75,763 expressions for 37,999 queried persons with bounding boxes on 10,702 images. There are 6,885 images with 48,509 expressions for training, 1,260 images with 9,074 expressions for validation and 2,557 images with 18,180 expressions for testing, respectively.

## Reference

- [Ref](https://ivipclab.github.io/publication_refcrowd/refcrowd/)
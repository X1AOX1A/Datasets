# CrowdCaption

## Data Features

![example](https://ivipclab.github.io/publication_crowdcaption/multicaption/featured_huad6674309315345f043ed3eea3dbcdd3_392693_720x2500_fit_q75_h2_lanczos.webp)

In CrowdCaption dataset, each image may contains multiple caption annotations, and each caption annotations has a detailed region grounding annotation. The location can be denoted as (x, y, w, h), where (x, y) denotes the top left of the region, w and h denote its width and height. The dataset annotations are provided in JSON format. Researchers can read the annotation files by the following Python 3 code:

```python
import json

path='./crowdcaption.json'
info_dict=json.load(open(path))['images']
image_name=info_dict['filename']                    # image name
split=info_dict['split']                            # image split in train, val or test
image_id=info_dict['imgid']                         # image id
human_position=info_dict['box']                     # single person localization annotations [x, y, w, h]
sentence_id=info_dict['dense_caption']['sentids']   # sentence id
region_id=info_dict['dense_caption']['region_ids']  # region id
sentences=info_dict['dense_caption']['sentences']   # all descriptions for each images
region_position=info_dict['dense_caption']['union_boxes'] # crowd region localization annotations [x, y, w, h] for each images
human_in_region_idx=info_dict['dense_caption']['sentences_region_idx'] # the human idx for who are in the corresponding region
```

## Data Example

Examples from `crowdcaption.json`:

![example-0](https://x1a-alioss.oss-cn-shenzhen.aliyuncs.com/SnippetsLab/202306241610930.jpg)

```
{
    "dataset": "crowd",
    "images": [
                {
                    "filepath": "crowdhuman2021", 
                    "filename": "00000000.jpg", 
                    "split": "test", 
                    "imgid": 0, 
                    "box": {
                        "0": {"x": 341.28, "y": 103.60000000000001, "width": 38.65, "height": 132.02}, 
                        "1": {"x": 492.29, "y": 98.93999999999998, "width": 60.83, "height": 131.79}, 
                        "2": {"x": 439.32, "y": 112.89, "width": 47.45, "height": 126.28}, 
                        "3": {"x": 396.67, "y": 133.32, "width": 27.04, "height": 81.82}, 
                        "4": {"x": 419.02, "y": 113.73, "width": 28.09, "height": 111.4}, 
                        "5": {"x": 491.17, "y": 173.05, "width": 71.59, "height": 59.31}, 
                        "6": {"x": 469.3, "y": 136.64, "width": 25.58, "height": 95.19}
                    }, 
                    "dense_caption": {
                        "sentids": [0, 1, 2, 3], 
                        "sentences": [
                            {
                                "tokens": ["there", "is", "a", "group", "of", "people", "under", "the", "tent", ".", "the", "woman", "on", "the", "far", "right", "is", "sitting", "on", "the", "ground", "."], 
                                "raw": "there is a group of people under the tent . the woman on the far right is sitting on the ground .", 
                                "imgid": 0, 
                                "sentids": 0
                            }, 
                            {
                                "tokens": ["sitting", "on", "the", "far", "right", "is", "a", "woman", ".", "a", "few", "people", "stands", "on", "her", "left", "under", "the", "white", "tent", "."], 
                                "raw": "sitting on the far right is a woman . a few people stands on her left under the white tent .", 
                                "imgid": 0, 
                                "sentids": 1
                            }, 
                            {
                                "tokens": ["there", "is", "a", "group", "of", "people", "on", "the", "right", "side", "of", "the", "beach", ".", "a", "man", "wearing", "socks", "stands", "outside", "the", "tent", "."], 
                                "raw": "there is a group of people on the right side of the beach . a man wearing socks stands outside the tent .", 
                                "imgid": 0, 
                                "sentids": 2
                            }, 
                            {
                                "tokens": ["there", "are", "some", "people", "standing", "and", "a", "woman", "sitting", "under", "the", "white", "tent", ".", "to", "their", "left", "are", "two", "men", "standing", "outside", "the", "tent", "."], 
                                "raw": "there are some people standing and a woman sitting under the white tent . to their left are two men standing outside the tent .", 
                                "imgid": 0, 
                                "sentids": 3
                            }
                        ], 
                        "sentences_region_idx": [
                            ["1", "2", "4", "5", "6"], 
                            ["1", "2", "4", "5", "6"], 
                            ["0", "1", "2", "3", "4", "5", "6"], 
                            ["0", "1", "2", "3", "4", "5", "6"]
                        ], 
                        "union_boxes": [
                            {"x": 419.02, "y": 98.93999999999998, "width": 143.74, "height": 140.23}, 
                            {"x": 419.02, "y": 98.93999999999998, "width": 143.74, "height": 140.23}, 
                            {"x": 341.28, "y": 98.93999999999998, "width": 221.48, "height": 140.23}, 
                            {"x": 341.28, "y": 98.93999999999998, "width": 221.48, "height": 140.23}
                        ], 
                        "region_id": [0, 0, 1, 1]
                    }
                }, 
                ...
    ]
}
```


## Download Links

To ensure the rational use of CrowdCaption dataset, researchers requires to sign [CrowdCaption Terms of Use](https://docs.google.com/forms/d/e/1FAIpQLSe-lXeeDFoMYqNa-TytDz8-2ipQ5kKYukDinahGpkGasmtWCA/viewform?usp=sf_link) as restrictions on access to dataset to privacy protection and use dataset for non-commercial research and/or educational purposes. If you have recieved access, you can download and extract our CrowdCaption Dataset.

## Download Script

The directory structure of the dataset is as follows:

```
CrowdCaption/
├── crowdcaption_images.zip
│  ├── crowdhuman2021/
│  │  ├── 00000000.jpg
│  │  ├── 000xxxxx.jpg
│  │  ├── 00011350.jpg
└── crowdcaption.json
```

## Statistics

![statistics](https://x1a-alioss.oss-cn-shenzhen.aliyuncs.com/SnippetsLab/202306241601931.png)

## Reference

- [Ref](https://ivipclab.github.io/publication_crowdcaption/multicaption/)
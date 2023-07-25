# Formatting CoCo Entities

## Raw Data Examples

<details>
<summary>Click to view the valid example</summary>

![coco entities](https://github.com/aimagelab/show-control-and-tell/raw/master/images/coco_entities.png)

```
"520208": {
    "a spoon sitting on some food in a bowl": {
        "det_sequences": ["spoon", "spoon", null, null, "food", "food", null, "bowl", "bowl"], 
        "noun_chunks": [
            ["a spoon", "spoon"], 
            ["some food", "food"], 
            ["a bowl", "bowl"]], 
        "detections": {
            "spoon": [[2, [0.0, 234.5964813232422, 477.697021484375, 479.20001220703125]], [14, [259.7029724121094, 215.28146362304688, 555.7696533203125, 395.4397277832031]]], 
            "food": [[0, [236.583984375, 0.0, 639.2000122070312, 375.694580078125]], [5, [68.67597961425781, 0.0, 542.5230102539062, 302.64239501953125]]], 
            "bowl": [[1, [12.056884765625, 32.955543518066406, 594.0037231445312, 464.70672607421875]]]}, 
        "split": "train"
    }, 
    "a bowl of food and a spoon held up that has eaten food": {
        "det_sequences": ["bowl", "bowl", null, "food", null, "spoon", "spoon", null, null, null, null, null, "food"], 
        "noun_chunks": [
            ["a bowl", "bowl"], 
            ["food", "food"], 
            ["a spoon", "spoon"], 
            ["food", "food"]], 
        "detections": {
            "bowl": [[1, [12.056884765625, 32.955543518066406, 594.0037231445312, 464.70672607421875]]], 
            "food": [[0, [236.583984375, 0.0, 639.2000122070312, 375.694580078125]], [5, [68.67597961425781, 0.0, 542.5230102539062, 302.64239501953125]]], 
            "spoon": [[2, [0.0, 234.5964813232422, 477.697021484375, 479.20001220703125]], [14, [259.7029724121094, 215.28146362304688, 555.7696533203125, 395.4397277832031]]]}, 
        "split": "train"
    }, 
    "a white bowl filled with mixed vegetables and a spoon": {
        "det_sequences": ["bowl", "bowl", "bowl", null, null, "potatoes", "potatoes", null, "spoon", "spoon"], 
        "noun_chunks": [["a white bowl", "bowl"], ["mixed vegetables", "potatoes"], ["a spoon", "spoon"]], "detections": {"bowl": [[1, [12.056884765625, 32.955543518066406, 594.0037231445312, 464.70672607421875]]], "potatoes": [[4, [261.80291748046875, 0.0, 639.2000122070312, 230.02053833007812]], [9, [26.407129287719727, 72.50532531738281, 400.67034912109375, 243.777099609375]]], "spoon": [[2, [0.0, 234.5964813232422, 477.697021484375, 479.20001220703125]], [14, [259.7029724121094, 215.28146362304688, 555.7696533203125, 395.4397277832031]]]}, "split": "train"
    }, 
    "there is a spoons resting in a bowl of food": {
        "det_sequences": [null, null, "spoon", "spoon", null, null, "bowl", "bowl", null, "food"], 
        "noun_chunks": [
            ["a spoons", "spoon"], 
            ["a bowl", "bowl"], 
            ["food", "food"]], 
        "detections": {
            "spoon": [[2, [0.0, 234.5964813232422, 477.697021484375, 479.20001220703125]], [14, [259.7029724121094, 215.28146362304688, 555.7696533203125, 395.4397277832031]]], 
            "food": [[0, [236.583984375, 0.0, 639.2000122070312, 375.694580078125]], [5, [68.67597961425781, 0.0, 542.5230102539062, 302.64239501953125]]], 
            "bowl": [[1, [12.056884765625, 32.955543518066406, 594.0037231445312, 464.70672607421875]]]}, 
        "split": "train"
    }, 
    "a close up of a spoon in a bowl of food": {
        "det_sequences": [null, null, null, null, "spoon", "spoon", null, "bowl", "bowl", null, "food"], 
        "noun_chunks": [
            ["a spoon", "spoon"], 
            ["a bowl", "bowl"], 
            ["food", "food"]], 
        "detections": {
            "spoon": [[2, [0.0, 234.5964813232422, 477.697021484375, 479.20001220703125]], [14, [259.7029724121094, 215.28146362304688, 555.7696533203125, 395.4397277832031]]], 
            "food": [[0, [236.583984375, 0.0, 639.2000122070312, 375.694580078125]], [5, [68.67597961425781, 0.0, 542.5230102539062, 302.64239501953125]]], 
            "bowl": [[1, [12.056884765625, 32.955543518066406, 594.0037231445312, 464.70672607421875]]]}, 
        "split": "train"}
    }
```

</details>

## Raw Data Analysis

We do a [data analysis](./notebooks/data_analysis.ipynb) on the CoCo Entities dataset, here are some statistics:

- Statistics of the CoCo Entities:

    ```
    # train [samples|images|captions]: [544926|113179|544926]
    # val   [samples|images|captions]: [4995|4995|24015]
    # test  [samples|images|captions]: [4995|4995|23940]
    ```

- For reference, the statistics of the  original CoCo Caption has:

    ```
    # train [samples|images|captions]: [566747|113287|566747]
    # val   [samples|images|captions]: [5000|5000|25010]
    # test  [samples|images|captions]: [5000|5000|25010]
    ```

- The difference between CoCo Entities and CoCo Caption:

    ```
    # train images in coco_ann but not in coco_entities: 108
    # train images in coco_entities but not in coco_ann: 0
    # val images in coco_ann but not in coco_entities: 5
    # val images in coco_entities but not in coco_ann: 0
    # test images in coco_ann but not in coco_entities: 5
    # test images in coco_entities but not in coco_ann: 0
    ```

## Formatting

We format the dataset into following format:

```
[
    {
        "image_id" (int): "image_file_id",  # unique for val/test splits
        "image" (str): "image_file_name",
        "annotations" (List[dict]): [
            {
                "caption": "caption",
                "entity": [
                    [start_idx, end_idx, x1, y1, x2, y2, entity_tag], 
                    # start_idx, end_idx (int): closed and opened index of the entity chunk in the caption
                    # x1, y1, x2, y2 (float): bbox coordinates of upper left and lower right corners
                    # entity_tag (str): entity tag of the entity chunk
                    ...
                ]
            },
            ... # mulitple annotations for the val/test/test_sct splits
        ],
    },
    ...
]
```

- Formatted example:

    <details>
    <summary>Click to view the formatted valid example</summary>

    ```
    [
        {
            "image": "val2014/COCO_val2014_000000184613.jpg", 
            "image_id": 184613, 
            "annotations": [
                {
                    "caption": "a child holding a flowered umbrella and petting a yak", 
                    "entity": [
                        [16, 35, 97.15347290039062, 19.300228118896484, 252.22230529785156, 156.1619873046875, "umbrella"], 
                        [48, 53, 287.6924133300781, 160.7919158935547, 458.9627990722656, 330.2914733886719, "goat"]
                    ]
                }, 
                {
                    "caption": "a young man holding an umbrella next to a herd of cattle", 
                    "entity": [
                        [0, 11, 1.792211890220642, 46.136470794677734, 84.72174835205078, 195.2536163330078, "man"], 
                        [20, 31, 97.15347290039062, 19.300228118896484, 252.22230529785156, 156.1619873046875, "umbrella"]
                    ]
                }, 
                {
                    "caption": "a young boy barefoot holding an umbrella touching the horn of a cow", 
                    "entity": [
                        [29, 40, 97.15347290039062, 19.300228118896484, 252.22230529785156, 156.1619873046875, "umbrella"], 
                        [50, 58, 304.73046875, 211.79176330566406, 348.4114990234375, 232.3231658935547, "horn"], 
                        [62, 67, 219.88400268554688, 184.03125, 499.52001953125, 335.44000244140625, "cow"]
                    ]
                }, 
                {
                    "caption": "a young boy with an umbrella who is touching the horn of a cow", 
                    "entity": [
                        [0, 11, 161.65379333496094, 68.76399230957031, 271.4734802246094, 303.5986633300781, "boy"], 
                        [17, 28, 97.15347290039062, 19.300228118896484, 252.22230529785156, 156.1619873046875, "umbrella"], 
                        [29, 32, 0.0, 0.0, 270.9290771484375, 234.3825225830078, "people"], 
                        [45, 53, 304.73046875, 211.79176330566406, 348.4114990234375, 232.3231658935547, "horn"], 
                        [57, 62, 219.88400268554688, 184.03125, 499.52001953125, 335.44000244140625, "cow"]
                    ]
                }, 
                {
                    "caption": "a boy holding an umbrella while standing next to livestock", 
                    "entity": [
                        [0, 5, 161.65379333496094, 68.76399230957031, 271.4734802246094, 303.5986633300781, "boy"], 
                        [14, 25, 97.15347290039062, 19.300228118896484, 252.22230529785156, 156.1619873046875, "umbrella"]
                    ]
                }
            ]
        },
        ... 
    ]
    ```

    </details>

- Formatting: to format the raw data, run the following command:

    ```
    export coco_entities_file="/root/Documents/DATASETS/CoCo_Entities/coco_entities_release.json"
    export coco_images_root="/root/Documents/DATASETS/MS_COCO/images"
    export save_path="/root/Documents/DATASETS/CoCo_Entities/CoCo_Entities_Formatted/annotations"
    python format_coco_entities.py --coco_entities_file $coco_entities_file --coco_images_root $coco_images_root --save_path $save_path
    ```
    - `coco_entities_file`: path to the raw CoCo Entities json file
    - `coco_images_root`: path to the CoCo images root directory
    - `save_path`: path to save the formatted CoCo Entities json path

- Splits: Apart from the original CoCo karpathy splits (`train`, `val`, `test`), we also have a `test_sct` split, which is used for the [Show, Control and Tell](https://arxiv.org/abs/1811.10652) task. The `test_sct` split is filteted and split from the original `test` split. Each sample consists of a image and mulit caption-entity pairs **with the same entity tag chunks**. For more details, please refer to the [Show, Control and Tell](https://arxiv.org/abs/1811.10652) paper.

- Statistics of the formatted CoCo Entities:

    ```
    # train    [samples|images|captions]: [544926|113179|544926]
    # val      [samples|images|captions]: [4995|4995|24015]
    # test     [samples|images|captions]: [4995|4995|23940]
    # test_sct [samples|images|captions]: [6858|3569|7790]
    ```

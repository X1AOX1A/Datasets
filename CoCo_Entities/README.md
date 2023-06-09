# COCO Entities

## Data Features

The annotation file contains a python dictionary structured as follows:
```
coco_entities_release.json
 └── <id_image>
      └── <caption>
           └── 'det_sequences'
           └── 'noun_chunks'
           └── 'detections'
           └── 'split'
```
In details, for each image-caption pair, we provide the following information:
* `det_sequences`, which contains a list of detection classes associated to each word of the caption (for an exact match with caption words, split the caption by spaces). `None` indicates the words that are not part of noun chunks, while `_` indicates noun chunk words for which an association with a detection in the image was not possible. 
* `noun_chunks`, which is a list of tuples representing the noun chunks of the captions associated with a detection in the image. Each tuple is composed by two elements: the first one represents the noun chunk in the caption, while the second is the detection class associated to that noun chunk.
* `detections`, which contains a dictionary with a number of elements equal to the number of detection classes associated with at least a noun chunk in the caption. For each detection class, it provides a list of tuples representing the image regions detected by Faster R-CNN re-trained on Visual Genome [1] and corresponding to that detection class. Each tuple is composed by the detection id and the corresponding boundig box in the form `[x1, y1, x2, y2]`. The detection id can be used to recover the detection feature vector from  the pre-computed features file [coco_detections.hdf5](https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/coco_detections.hdf5) (~53.5 GB). See the demo section below for more details. 
* `split`, which indicates the dataset split of that sample (_i.e._ train, val or test) following the COCO splits provided by [2].

## Data Example

![coco entities](https://github.com/aimagelab/show-control-and-tell/raw/master/images/sample_results.png)

```
520208": {
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

## Download Links

If you want to use only the annotations of our COCO Entities dataset, you can download the annotation file [coco_entities_release.json](https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/coco_entities_release.json) (~403 MB).

## Download Script

```shell
cd CoCo_Entities
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
watch -n 1 tail nohup.out
```

- The downloaded files are structured as follows:

```
CoCo_Entities/
    coco_entities_release.json  404M
```

## Statistics

NA

## Reference

- [Ref](https://github.com/aimagelab/show-control-and-tell/tree/master#coco-entities-1)
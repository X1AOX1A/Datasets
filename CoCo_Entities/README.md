# COCO Entities
If you want to use only the annotations of our COCO Entities dataset, you can download the annotation file [coco_entities_release.json](https://ailb-web.ing.unimore.it/publicfiles/drive/show-control-and-tell/coco_entities_release.json) (~403 MB).

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

Note that this annotation file includes all image-caption pairs for which at least one noun chunk-detection association has been found. However, in validation and testing phase of our controllable captioning model, we dropped all captions with empty region sets (_i.e._ those captions with at least one `_` in the `det_sequences` field). 

![coco entities](https://x1a-alioss.oss-cn-shenzhen.aliyuncs.com/SnippetsLab/coco_entities.png)

[Ref](https://github.com/aimagelab/show-control-and-tell/tree/master#coco-entities-1)
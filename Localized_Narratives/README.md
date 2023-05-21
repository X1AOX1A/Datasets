# Localized Narratives

## Full Localized Narratives

- Here you can download the full set of Localized Narratives 
- Large files are split in shards (a list of them will appear when you click below). 
- In parantheses, the number of Localized Narratives in each split. Please note that some images have more than one Localized Narrative annotation, e.g. 5k images in COCO are annotated 5 times.

### Download Links

- Open Images

  - Train (507,444): 
      [0](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00000-of-00010.jsonl)
      [1](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00001-of-00010.jsonl)
      [2](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00002-of-00010.jsonl)
      [3](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00003-of-00010.jsonl)
      [4](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00004-of-00010.jsonl)
      [5](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00005-of-00010.jsonl)
      [6](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00006-of-00010.jsonl)
      [7](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00007-of-00010.jsonl)
      [8](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00008-of-00010.jsonl)
      [9](https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-00009-of-00010.jsonl)
  - Valid (41,691):
      [0](https://storage.googleapis.com/localized-narratives/annotations/open_images_validation_localized_narratives.jsonl)
  - Test (126,020):
      [0](https://storage.googleapis.com/localized-narratives/annotations/open_images_test_localized_narratives.jsonl)

- COCO
  - Train (134,272)
    [0](https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-00000-of-00004.jsonl)
    [1](https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-00001-of-00004.jsonl)
    [2](https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-00002-of-00004.jsonl)
    [3](https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-00003-of-00004.jsonl)
  - Valid (8,573)
    [0](https://storage.googleapis.com/localized-narratives/annotations/coco_val_localized_narratives.jsonl)

- Flickr30k
  - Train (30,546)
    [0](https://storage.googleapis.com/localized-narratives/annotations/flickr30k_train_localized_narratives.jsonl)
  - Valid (1,009)
    [0](https://storage.googleapis.com/localized-narratives/annotations/flickr30k_val_localized_narratives.jsonl)
  - Test (1,023)
    [0](https://storage.googleapis.com/localized-narratives/annotations/flickr30k_test_localized_narratives.jsonl)

- ADE20k
  - Train (20,476)
    [0](https://storage.googleapis.com/localized-narratives/annotations/ade20k_train_localized_narratives.jsonl)
  - Valid (2,053)
    [0](https://storage.googleapis.com/localized-narratives/annotations/ade20k_validation_localized_narratives.jsonl)


### Download Script

- `download_datasets.sh`:

```shell
#!/bin/bash

# Create directories
mkdir "Open_Image"
mkdir "COCO"
mkdir "Flickr30k"
mkdir "ADE20k"

# Download Open Images
mkdir "Open_Image/train"
for i in {0..9}; do
    wget -P "Open_Image/train" "https://storage.googleapis.com/localized-narratives/annotations/open_images_train_v6_localized_narratives-0000${i}-of-00010.jsonl"
done

mkdir "Open_Image/valid"
wget -P "Open Image/valid" "https://storage.googleapis.com/localized-narratives/annotations/open_images_validation_localized_narratives.jsonl"

mkdir "Open_Image/test"
wget -P "Open Image/test" "https://storage.googleapis.com/localized-narratives/annotations/open_images_test_localized_narratives.jsonl"

# Download COCO
mkdir "COCO/train"
for i in {0..3}; do
    wget -P "COCO/train" "https://storage.googleapis.com/localized-narratives/annotations/coco_train_localized_narratives-0000${i}-of-00004.jsonl"
done

mkdir "COCO/valid"
wget -P "COCO/valid" "https://storage.googleapis.com/localized-narratives/annotations/coco_val_localized_narratives.jsonl"

# Download Flickr30k
mkdir "Flickr30k/train"
wget -P "Flickr30k/train" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_train_localized_narratives.jsonl"

mkdir "Flickr30k/valid"
wget -P "Flickr30k/valid" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_val_localized_narratives.jsonl"

mkdir "Flickr30k/test"
wget -P "Flickr30k/test" "https://storage.googleapis.com/localized-narratives/annotations/flickr30k_test_localized_narratives.jsonl"

# Download ADE20k
mkdir "ADE20k/train"
wget -P "ADE20k/train" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_train_localized_narratives.jsonl"

mkdir "ADE20k/valid"
wget -P "ADE20k/valid" "https://storage.googleapis.com/localized-narratives/annotations/ade20k_validation_localized_narratives.jsonl"
```

Excute:

```shell
chmod +x download_datasets.sh
nohup ./download_datasets.sh >nohup.out& 2>&1
```

## File formats

The annotations are in JSON Lines format, that is, each line of the file is an independent valid JSON-encoded object. The largest files are split into smaller sub-files (shards) for ease of download. Since each line of the file is independent, the whole file can be reconstructed by simply concatenating the contents of the shards.

Each line represents one Localized Narrative annotation on one image by one annotator and has the following fields:

- `dataset_id`: String identifying the dataset and split where the image belongs, e.g. mscoco_val2017.
- `image_id`: String identifier of the image, as specified on each dataset.
- `annotator_id`: Integer number uniquely identifying each annotator.
- `caption`: Image caption as a string of characters.
- `timed_caption`: List of timed utterances, i.e. {utterance, start_time, end_time} where utterance is a word (or group of words) and (start_time, end_time) is the time during which it was spoken, with respect to the start of the recording.
- `traces`: List of trace segments, one between each time the mouse pointer enters the image and goes away from it. Each trace segment is represented as a list of timed points, i.e. {x, y, t}, where x and y are the normalized image coordinates (with origin at the top-left corner of the image) and t is the time in seconds since the start of the recording. Please note that the coordinates can go a bit beyond the image, i.e. <0 or >1, as we recorded the mouse traces including a small band around the image.
- `voice_recording`: Relative URL path with respect to https://storage.googleapis.com/localized-narratives/voice-recordings where to find the voice recording (in OGG format) for that particular image.
Below a sample of one Localized Narrative in this format:

```json
{
  dataset_id: 'mscoco_val2017',
  image_id: '137576',
  annotator_id: 93,
  caption: 'In this image there are group of cows standing and eating th...',
  timed_caption: [{'utterance': 'In this', 'start_time': 0.0, 'end_time': 0.4}, ...],
  traces: [[{'x': 0.2086, 'y': -0.0533, 't': 0.022}, ...], ...],
  voice_recording: 'coco_val/coco_val_137576_93.ogg'
}
```

- [Ref](https://google.github.io/localized-narratives/)
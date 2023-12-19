# Densely Captioned Images

## Data Features

The Densely Captioned Images dataset, or DCI, consists of 8021 images from [SA-1B](https://ai.meta.com/datasets/segment-anything/), each with a complete description aiming to capture the full visual detail of what is present in the image. Much of the description is directly aligned to submasks of the image.

![Water Pump example from Densely Captioned Images](./docs/images/Example1New.png)

An example is shown above. In the top left we see the full image of a water pump, with an associated description. The italicized section is collected as a ‘standard caption’, aiming to summarize the full image in about a sentence. The remainder of that first description contains details about the relationship between visible entities in the image, as well as in-depth descriptions of regions that are not described as part of the submasks. All other text describing the image is all associated with submasks of the image. Each submask has its own label (not pictured) and description, and may also contain further submasks. Here for instance we see submasks for windows and balconies as being contained in the submask capturing three buildings in the background.

## Data

### CLIP-ready
We provide easy data-loader utilities for the CLIP-ready version of the densely captioned images dataset, wherein all Captions have LLaMA2-generated summaries and negatives that fit inside of the CLIP context limit.

```python
from densely_captioned_images.dataset.impl import get_clip_ready_ds, DenseCaptionedDataset
train_ds: DenseCaptionedDataset = get_clip_ready_ds('train')
valid_ds: DenseCaptionedDataset = get_clip_ready_ds('valid')
```

### Demo

You can preview data from the DCI dataset by running the explorer script:
```bash
cd /data/DATASETS/DCI
conda activate densecaps
pip install flask
python explorer/run_server.py <port>
```

This shows the complete data available from within the `DenseCaptionedImage` class at `http://localhost:port`:

![View of DCI explorer](./docs/images/Explorer.png)

In this view, you can navigate to image by index or by specific ID. The `[prev]` and `[next]` buttons can be used to directly parse through. On screen is the complete description of the image, as well as all submasks. Hovering over words in the text highlights the corresponding mask in the image, as is done here for *"Top most green tree leaves"*.

### Data Sample

The `DenseCaptionedImage` class acts as a wrapper around the stored data json, which has the following format:
```yaml
{
    "image": "relative-image-path.jpg",
    "short_caption": "A standard short-form caption for the image",
    "mask_data": {
      "[mask_key]": {
        "idx": "[mask_key]",                        # Self-reference into mapping
        "outer_mask": "iVBORw0KGgoAAAANSUhE.....",  # base64 encoding of the binary mask for this segment
        "mask_quality": 0,                          # one of 0, 1, or 2 for "ok", "low-quality/uninteresting", or "bad" respectively
        "label": "A short label for the given mask", # omitted if "bad" quality
        "caption": "A long descriptive caption for this given mask", # only for "ok" masks
        "parent": "other_mask_key",                 # either the parent mask id in the tree, or -1 if parent is the base image
        "requirements": ["list", "of", "children", "masks"] # mask IDs for children masks
        "bounds": [[0, 0], [500, 500]]              # TopLeft & BottomRight coords of mask bounds
        "area": 123,                                # mask size in pixels 
      },
      # ...
    },
    "mask_keys": ["list", "of", "mask_keys", "into", "mask_data"],
    "extra_caption": "Additional long form caption that may catch additional information about layout or from from missing masks",
    "summaries": {
        "base": ["list", "of", "generated", "summaries"],
        # ...
        "[mask_key]": ["list", "of", "generated", "summaries"],
        # ...
    },
    "negatives": {
        # ...
        "[mask_key]": {
            # ...
            "[negative_type]": ["list", "of", "negatives", "generated", "of", "type"],
            # ...
        },
        # ...
    }
}
```

## (CLIP-ready) Densely Captioned Images Test set

The Densely Captioned Images test set comes in a few variations:
- **All Submasks**: Pulls images and all subimages from the test set, and uses their first captions. Key: `all_swaps`
- **All Submasks Pick 5**: Pulls images and all subimages from the test set, and uses their first 5 captions. Key: `all_swaps_pick5`
- **Base**: Only pulls the 112 base images from the test set, alongside their first captions. Key: `base_swaps`
- **Hardest**: Use the same imageset as `all_swaps`, but hardest negative of all generated based on CLIP score. Key: `all_hardest`

All tests report both the CLIP-correct (correct caption prediction compared to rest of batch) and Negative-correct (correct caption prediction compared to a generated negative).

### Usage

You can also directly reproduce the DCI results for CLIP with the following:
```bash
python dataset/densely_captioned_images/dataset/scripts/run_clip_dense_cap_eval.py 
```

You can also reproduce our results on provided DCI-trained models by running the following in a python shell from the project root.
```python
from densely_captioned_images.dataset.scripts.run_clip_dense_cap_eval import run_dense_cap_on_lora
run_dense_cap_on_lora('models/dci_pick1')
run_dense_cap_on_lora('models/dci_pick1_nl0')
```

So long as you can wrap a model in `CLIPModel`, you can use the `run_dense_cap_on_model` function instead to test your own models.


## Download Script

```shell
cd /data/DATASETS/
git clone git@github.com:facebookresearch/DCI.git
cd /data/DATASETS/DCI
conda create -n densecaps python=3.10
conda activate densecaps
cd dataset
pip install -e .

cd /data/DATASETS/DCI
python dataset/densely_captioned_images/dataset/scripts/download.py
```

- The downloaded files are structured as follows:

    ```
    DCI/
    |-- [9.3G]  data
    |   `-- [9.3G]  densely_captioned_images
    |       |-- [800M]  annotations
    |       |-- [1004M] complete
    |       |-- [7.6G]  photos
    |       `-- [157K]  splits.json
    ```

## Statistics

![statistics](../Examples/DCI/statistics.png)

## Reference

- [Ref](https://github.com/facebookresearch/DCI)
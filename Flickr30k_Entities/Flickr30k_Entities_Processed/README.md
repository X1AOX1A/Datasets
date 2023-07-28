# Processing Flickr30K Entities

We processed the dataset into following format:

```
[
    {
        "image_id" (int): image_id,
        "image" (str): "image_file_name",    
        "image_size" (list[int]): [width, height, depth],
        "annotations" (list[dict]): [
            {
                "caption" (str): "caption_text",
                "entities" (list[dict]): [
                    {
                        "start_idx": start_idx,             # closed
                        "end_idx": end_idx,                 # opened
                        "noun_chunk": "noun_chunk",         # associated noun chunk
                        "entity_tag": ["entity_tag", ...],  # associated entity tags
                        "box_id": "box_id",                 # associated box id
                    }, 
                    ...
                ],
            },
            ... # mulitple annotations for the val/test/val_grouped/test_grouped splits   
        ],
        "boxes":{
            "box_id": [[x_min, y_min, x_max, y_max], ...],
            "box_id": [[x_min, y_min, x_max, y_max], ...],
            ...
        }
    },
    ...
]    
```

### Splits

- Flickr30K karpathy splits: The original Flickr30K karpathy splits (`train`, `val`, `test`)
- Grouped splits: Apart from the the original splits, we further add `val_grouped` and  `test_grouped` splits, which are used for the [Show, Control and Tell](https://arxiv.org/abs/1811.10652) task. 
    - The `val_grouped` and `test_grouped` splits are filteted and split from the original `val` and `test` split, respectively.
    - Each sample consists of a image and mulit caption-entity pairs **with the same bbox reference sequence**. For more details, please refer to the [Show, Control and Tell](https://arxiv.org/abs/1811.10652) paper.

### Statistics

- Statistics of the processed Flickr30K Entities:

    ```
    # train        [samples|images|captions]: [148166|29781|148166]
    # val          [samples|images|captions]: [1000|1000|4986]
    # test         [samples|images|captions]: [999|999|4969]
    # val_grouped  [samples|images|captions]: [4178|1000|4986]
    # test_grouped [samples|images|captions]: [4054|999|4969]
    ```

### Process Procedure

- [process_train](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L227): For `train` set,  we 
    1. first filter out those entity without bbox reference (e.g., None and "_") ([drop_no_box_entity](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L202)). 
        - If all entity in the annotation are filtered out, we drop the annotation. (*This may decrease the number of captions*)
        - If all annotations are dropped, we drop the sample. (*This may decrease the number of images*)
    2. then we split annotations into caption-annotation pairs.

- [process_val](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L252): For `val` and `test` set, we 
    1. filter out those entity without bbox reference (e.g., None and "_") ([drop_no_box_entity](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L202)).
        - If all entity in the annotation are filtered out, we drop the annotation. (*This may decrease the number of captions*)
        - If all annotations are dropped, we drop the sample. (*This may decrease the number of images*)

- [process_val_grouped](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L275): For `val_grouped` and `test_grouped` set, we 
    1. first filter out those entity without bbox reference (e.g., None and "_") ([drop_no_box_entity](https://github.com/X1AOX1A/Datasets/blob/main/Flickr30k_Entities/Flickr30k_Entities_Processed/process_flickr30k_entities.py#L202)).
        - *This may further decrease the number of captions and images.*
    3. then, we group the annotations with the same bbox reference sequence and further split them into samples, as [SCT](https://github.com/aimagelab/show-control-and-tell/blob/master/test_region_sequence.py#L133) done.
        - *This may increase the number of samples, as we split the annotations with the same bbox reference sequence into multiple samples.*


### Process the Flickr30k Entities

- To format the raw data, run the following command:

    ```
    export flickr_entities_root="/root/Documents/DATASETS/Flickr30k_Entities"
    export save_path="/root/Documents/DATASETS/CoCo_Entities/CoCo_Entities_Processed/annotations"
    python process_flickr30k_entities.py --flickr_entities_root $flickr_entities_root --save_path $save_path
    ```
    - `flickr_entities_root`: path to the Flickr30K Entities root directory
    - `save_path`: path to save the processed CoCo Entities json path

- The processed files are structured as follows: 

    ```
    save_path/
    |-- [ 347]  info.json
    |-- [2.3M]  test.json
    |-- [3.4M]  test_grouped.json
    |-- [112M]  train.json
    |-- [2.3M]  val.json
    `-- [3.5M]  val_grouped.json
    ```

### Formatted example:

- Training example
    <details>
    <summary>Click to view the example</summary>

    ```
    [
        {
            'image_id': 3359636318, 
            'image': '3359636318.jpg', 
            'image_size': [500, 334, 3], 
            'annotations': [
                {
                    'caption': 'Two people are talking outside of the video game shop next door to the mobile phone store .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 10, 'noun_chunk': 'Two people', 'entity_tag': ['people'], 'box_id': '112630'}, 
                        {'start_idx': 34, 'end_idx': 53, 'noun_chunk': 'the video game shop', 'entity_tag': ['scene'], 'box_id': '112632'},
                        {'start_idx': 67, 'end_idx': 89, 'noun_chunk': 'the mobile phone store', 'entity_tag': ['scene'], 'box_id': '112631'}
                    ]
                }
            ], 
            'boxes': {
                '112625': [[46, 182, 105, 333], [143, 165, 207, 333], [237, 140, 296, 305], [449, 142, 485, 267], [192, 185, 232, 262]], 
                '112630': [[46, 182, 105, 333], [143, 165, 207, 333]], 
                '112626': [[2, 212, 499, 333]], 
                '112627': [[191, 0, 498, 230], [1, 0, 190, 307]], 
                '112631': [[191, 0, 498, 230]], 
                '112632': [[0, 54, 168, 307]]
            }
        },
        {
            'image_id': 3359636318, 
            'image': '3359636318.jpg', 
            'image_size': [500, 334, 3], 
            'annotations': [
                {
                    'caption': 'A group of people are standing in front of some stores .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 17, 'noun_chunk': 'A group of people', 'entity_tag': ['people'], 'box_id': '112625'}, 
                        {'start_idx': 43, 'end_idx': 54, 'noun_chunk': 'some stores', 'entity_tag': ['scene'], 'box_id': '112627'}
                    ]
                }
            ], 
            'boxes': {
                '112625': [[46, 182, 105, 333], [143, 165, 207, 333], [237, 140, 296, 305], [449, 142, 485, 267], [192, 185, 232, 262]], 
                '112630': [[46, 182, 105, 333], [143, 165, 207, 333]], 
                '112626': [[2, 212, 499, 333]], 
                '112627': [[191, 0, 498, 230], [1, 0, 190, 307]], 
                '112631': [[191, 0, 498, 230]], 
                '112632': [[0, 54, 168, 307]]
            }
        }
    ]
    ```
    </details>

- Test example
    <details>
    <summary>Click to view the example</summary>

    ```
    [
        {
            'image_id': 1016887272, 
            'image': '1016887272.jpg', 
            'image_size': [333, 500, 3], 
            'annotations': [
                {
                    'caption': 'Several climbers in a row are climbing the rock while the man in red watches and holds the line .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 16, 'noun_chunk': 'Several climbers', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 39, 'end_idx': 47, 'noun_chunk': 'the rock', 'entity_tag': ['other'], 'box_id': '548'}, 
                        {'start_idx': 54, 'end_idx': 61, 'noun_chunk': 'the man', 'entity_tag': ['people'], 'box_id': '549'},
                        {'start_idx': 65, 'end_idx': 68, 'noun_chunk': 'red', 'entity_tag': ['clothing'], 'box_id': '550'}, 
                        {'start_idx': 87, 'end_idx': 95, 'noun_chunk': 'the line', 'entity_tag': ['other'], 'box_id': '551'}
                    ]
                }, 
                {
                    'caption': 'Seven climbers are ascending a rock face whilst another man stands holding the rope .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 14, 'noun_chunk': 'Seven climbers', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 29, 'end_idx': 40, 'noun_chunk': 'a rock face', 'entity_tag': ['bodyparts'], 'box_id': '548'}, 
                        {'start_idx': 48, 'end_idx': 59, 'noun_chunk': 'another man', 'entity_tag': ['people'], 'box_id': '549'}, 
                        {'start_idx': 75, 'end_idx': 83, 'noun_chunk': 'the rope', 'entity_tag': ['other'], 'box_id': '551'}
                    ]
                }, 
                {
                    'caption': 'A group of people are rock climbing on a rock climbing wall .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 17, 'noun_chunk': 'A group of people', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 39, 'end_idx': 59, 'noun_chunk': 'a rock climbing wall', 'entity_tag': ['other'], 'box_id': '548'}
                    ]
                }, 
                {
                    'caption': 'A group of people climbing a rock while one man belays', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 17, 'noun_chunk': 'A group of people', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 27, 'end_idx': 33, 'noun_chunk': 'a rock', 'entity_tag': ['other'], 'box_id': '548'}, 
                        {'start_idx': 40, 'end_idx': 47, 'noun_chunk': 'one man', 'entity_tag': ['people'], 'box_id': '549'}
                    ]
                }, 
                {
                    'caption': 'A collage of one person climbing a cliff .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 23, 'noun_chunk': 'A collage of one person', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 33, 'end_idx': 40, 'noun_chunk': 'a cliff', 'entity_tag': ['scene'], 'box_id': '548'}
                    ]
                }
            ], 
            'boxes': {
                '547': [[193, 369, 230, 453], [207, 303, 255, 383], [187, 238, 226, 306], [164, 204, 204, 260], [176, 163, 228, 214], [166, 132, 208, 183], [161, 101, 203, 145]], 
                '548': [[0, 53, 332, 499]], 
                '549': [[73, 301, 180, 499]], 
                '550': [[79, 377, 141, 434], [74, 326, 124, 381]], 
                '551': [[118, 80, 187, 487]]
            }
        },
        ...
    ]   
    ```
    </details>

- Test grouped example
    <details>
    <summary>Click to view the example</summary>

    ```
    [
        {
            'image_id': 1016887272, 
            'image': '1016887272.jpg', 
            'image_size': [333, 500, 3], 
            'annotations': [
                {
                    'caption': 'Several climbers in a row are climbing the rock while the man in red watches and holds the line .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 16, 'noun_chunk': 'Several climbers', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 39, 'end_idx': 47, 'noun_chunk': 'the rock', 'entity_tag': ['other'], 'box_id': '548'}, 
                        {'start_idx': 54, 'end_idx': 61, 'noun_chunk': 'the man', 'entity_tag': ['people'], 'box_id': '549'}, 
                        {'start_idx': 65, 'end_idx': 68, 'noun_chunk': 'red', 'entity_tag': ['clothing'], 'box_id': '550'}, 
                        {'start_idx': 87, 'end_idx': 95, 'noun_chunk': 'the line', 'entity_tag': ['other'], 'box_id': '551'}
                    ]
                }
            ], 
            'boxes': {
                '547': [[193, 369, 230, 453], [207, 303, 255, 383], [187, 238, 226, 306], [164, 204, 204, 260], [176, 163, 228, 214], [166, 132, 208, 183], [161, 101, 203, 145]], 
                '548': [[0, 53, 332, 499]], 
                '549': [[73, 301, 180, 499]], 
                '550': [[79, 377, 141, 434], [74, 326, 124, 381]], 
                '551': [[118, 80, 187, 487]]
            }
        },
            
        {
            'image_id': 1016887272, 
            'image': '1016887272.jpg', 
            'image_size': [333, 500, 3], 
            'annotations': [
                {
                    'caption': 'Seven climbers are ascending a rock face whilst another man stands holding the rope .', 
                    'entities': [
                        {'start_idx': 0, 'end_idx': 14, 'noun_chunk': 'Seven climbers', 'entity_tag': ['people'], 'box_id': '547'}, 
                        {'start_idx': 29, 'end_idx': 40, 'noun_chunk': 'a rock face', 'entity_tag': ['bodyparts'], 'box_id': '548'}, 
                        {'start_idx': 48, 'end_idx': 59, 'noun_chunk': 'another man', 'entity_tag': ['people'], 'box_id': '549'}, 
                        {'start_idx': 75, 'end_idx': 83, 'noun_chunk': 'the rope', 'entity_tag': ['other'], 'box_id': '551'}
                    ]
                }
            ], 
            'boxes': {
                '547': [[193, 369, 230, 453], [207, 303, 255, 383], [187, 238, 226, 306], [164, 204, 204, 260], [176, 163, 228, 214], [166, 132, 208, 183], [161, 101, 203, 145]], 
                '548': [[0, 53, 332, 499]], 
                '549': [[73, 301, 180, 499]], 
                '550': [[79, 377, 141, 434], [74, 326, 124, 381]], 
                '551': [[118, 80, 187, 487]]
            }
        }
    ]
    ```

    </details>
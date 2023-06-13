import os
import re
import json
from tqdm import tqdm

class FilterCoCoAnnEntities:

    def __init__(self, ann_root, entities_path):
        self.coco_annotates = self.read_coco_annotations(ann_root)
        self.coco_entities = self.read_coco_entities(entities_path)
        self.coco_annotates_filtered = {"train": [], "val": [], "test": []}
        self.coco_entities_filtered = {"train": [], "val": [], "test": []}

        # only keep the records with all entities found
        self.filter_train()
        self.filter_val("val")
        self.filter_val("test")

    def read_coco_annotations(self, ann_root):
        # Read the annotations of MS COCO dataset.
        # Args:
        #     ann_root: the root path of annotations, e.g. "coco/annotations"
        # Returns:
        #     annotations: a dict of annotations, including train, val, test.        
        print("Reading CoCo annotations...")
        splits = {
            "train": 'coco_karpathy_train.json',
            "val": 'coco_karpathy_val.json',
            "test": 'coco_karpathy_test.json',
        }
        
        annotations = {}
        for split, file in splits.items():
            data = json.load(
                open(os.path.join(ann_root, file), "r")
            )
            # modify the "image_id"
            for i, ann in enumerate(data):
                data[i]["image_id"] = str(int(ann["image"].split('_')[-1].split('.')[0]))
            
            annotations[split] = data                
        return annotations

    def read_coco_entities(self, entities_path):
        # Read the entities of MS COCO dataset.
        # Args:
        #     entities_path: the path to entities, e.g. "coco_entities_release.json"
        # Returns:
        #     entities: a dict of entities, including train, val, test.
        # Sample:
        # print(self.coco_entities["train"]["522418"])
        # {
        #     'a woman marking a cake with the back of a chefs knife': {
        #     'det_sequences': ['_','_', None, '_', '_', None, '_', '_', None, 'knife', 'knife', 'knife'],
        #     'noun_chunks': [['a woman', '_'], ['a cake', '_'], ['the back', '_'], ['a chefs knife', 'knife']],
        #     'detections': {
        #         'knife': [[11, [272.3580017089844, 406.91986083984375, 460.58953857421875, 472.1031799316406]]]},
        #     'split': 'train'
        #     }
        # }
        print("Reading CoCo entities...")
        raw_entities = json.load(open(entities_path, "r"))
        entities = {"train": {}, "val": {}, "test": {}}
        for image_id, anns in raw_entities.items():
            split = list(anns.values())[0]["split"]
            entities[split][image_id] = anns
        return entities
    
    def clean_text(self, string):
        string = string.lower()
        string = re.sub(r"[^a-z]+", "", string)
        string = string.strip()
        return string

    def caption_matching(self, caption, entities):
        clean_caption = self.clean_text(caption)
        clean_entities_captions = [self.clean_text(entity) for entity in entities.keys()]
        for idx, enti_cap in enumerate(clean_entities_captions):
            if clean_caption==enti_cap:
                # return the matched caption
                return list(entities.keys())[idx]
        return None

    def filter_train(self):
        print("\nFiltering train split...")
        counter = 0
        for annotate in tqdm(self.coco_annotates["train"]):
            image_id = annotate["image_id"]
            if image_id in self.coco_entities["train"]:
                caption = annotate["caption"]
                entities = self.coco_entities["train"][image_id]
                matched_caption = self.caption_matching(caption, entities)
                if matched_caption:
                    counter += 1
                    matched_entities = entities[matched_caption]
                    self.coco_annotates_filtered["train"].append(annotate)
                    self.coco_entities_filtered["train"].append({caption: matched_entities})

        print("#Filtered train samples: {} out of {}".format(counter, len(self.coco_annotates["train"])))

    def filter_val(self, split="val"):
        print("\nFiltering {} split...".format(split))
        counter = 0
        for annotate in tqdm(self.coco_annotates[split]):
            image_id = annotate["image_id"]
            if image_id in self.coco_entities[split]:
                caption_list = annotate["caption"]                
                entities = self.coco_entities[split][image_id]  # {image_id: entities dict of all captions}
                matched_entities_dict = {}                      # {caption: corresponding entities}
                for caption in caption_list:
                    matched_caption = self.caption_matching(caption, entities)
                    if not matched_caption:
                        break   # we only keep the samples with all entities found
                    else:
                        matched_entities_dict[caption] = entities[matched_caption]

                # we only keep the samples with all entities found
                if len(caption_list)==len(matched_entities_dict):
                    counter += 1
                    self.coco_annotates_filtered[split].append(annotate)
                    self.coco_entities_filtered[split].append(matched_entities_dict)
        
        print("#Filtered {} samples: {} out of {}".format(split, counter, len(self.coco_annotates[split])))
        
    def save_coco_filtered(self, save_path):
        # Save the filtered annotations and entities
        # Args:
        #     save_path: the path to save the filtered annotations and entities
        # Returns:
        #    save_path
        #    ├── annotations
        #    │   ├── coco_karpathy_train.json
        #    │   ├── coco_karpathy_val.json
        #    │   └── coco_karpathy_test.json
        #    └── entities
        #        ├── coco_entities_train.json
        #        ├── coco_entities_val.json
        #        └── coco_entities_test.json

        # save the filtered annotations
        print("\nSaving the filtered CoCo annotations...")
        annotations_path = os.path.join(save_path, "annotations")
        os.makedirs(annotations_path, exist_ok=True)
        annotations_splits = {
            "train": 'coco_karpathy_train.json',
            "val": 'coco_karpathy_val.json',
            "test": 'coco_karpathy_test.json',
        }      
        for split, file in annotations_splits.items():
            print("- Saving {} to {}...".format(split, os.path.join(annotations_path, file)))
            json.dump(
                self.coco_annotates_filtered[split], 
                open(os.path.join(annotations_path, file), "w")
            )

        # save the filtered entities
        print("\nSaving the filtered CoCo entities...")
        entities_path = os.path.join(save_path, "entities")
        os.makedirs(entities_path, exist_ok=True)
        entities_splits = {
            "train": 'coco_entities_train.json',
            "val": 'coco_entities_val.json',
            "test": 'coco_entities_test.json',
        }
        for split, file in entities_splits.items():
            print("- Saving {} to {}...".format(split, os.path.join(entities_path, file)))
            json.dump(
                self.coco_entities_filtered[split], 
                open(os.path.join(entities_path, file), "w")
            )        

        print("Done!")
    
if __name__ == "__main__":
    ann_root = "/root/Documents/DATASETS/MS_COCO/annotations"
    entities_path = "/root/Documents/DATASETS/CoCo_Entities/coco_entities_release.json"
    save_path = "/root/Documents/DATASETS/CoCo_Entities/coco_filterd"
    
    coco_filtered = FilterCoCoAnnEntities(ann_root, entities_path)
    coco_filtered.save_coco_filtered(save_path)
import os
import sys
import json
import numpy as np
from PIL import Image
from tqdm import tqdm
from copy import deepcopy as copy

try:
    from loguru import logger as logging
    logging.add(sys.stderr, filter="my_module")
except ImportError:
    import logging

def get_entities(caption, det_sequences):
    """Get the start and end indices of entities in the caption
    Args:
        caption (str): the caption of CoCo Entities, 
            e.g. "a restaurant has modern wooden tables and chairs"
        det_sequences (list): list of entity tags, 
            e.g. ['_', '_', None, 'table', 'table', 'table', None, 'chairs']
    Returns:
        entities (list): [{"start_idx": int, "end_idx": int, "noun_chunk": str, "entity_tag": List[str], "box_id": str}]            
            e.g. 
            [{'start_idx': 0, 'end_idx': 1, 'noun_chunk': 'a', 'entity_tag': ['_'], 'box_id': '_'}, 
            {'start_idx': 13, 'end_idx': 16, 'noun_chunk': 'has', 'entity_tag': [None], 'box_id': None}, 
            {'start_idx': 17, 'end_idx': 37, 'noun_chunk': 'modern wooden tables', 'entity_tag': ['table'], 'box_id': 'table'}, 
            {'start_idx': 38, 'end_idx': 41, 'noun_chunk': 'and', 'entity_tag': [None], 'box_id': None}, 
            {'start_idx': 42, 'end_idx': 48, 'noun_chunk': 'chairs', 'entity_tag': ['chairs'], 'box_id': 'chairs'}]
    """
    off_set, prev_end_idx = 0, 0
    prev_entity_tag = None
    start_idxs, end_idxs = [], []
    entity_tags = []
    caption_word = caption.split(" ")
    assert len(caption_word) == len(det_sequences)
    for i, (word, entity_tag) in enumerate(zip(caption_word, det_sequences)):
        if entity_tag == prev_entity_tag:
            end_idx = len(word) if i==0 else min(prev_end_idx+len(word)+1, len(caption))
            if entity_tag not in [None, "_"]:
                end_idxs[-1] = end_idx
        else:
            start_idx = off_set
            end_idx = start_idx + len(word)            
            start_idxs.append(start_idx)
            end_idxs.append(end_idx)
            entity_tags.append(entity_tag)
            prev_entity_tag = entity_tag
        off_set = end_idx+1
        prev_end_idx = end_idx
    
    entities = []
    for start_idx, end_idx, entity_tag in zip(start_idxs, end_idxs, entity_tags):
        entity = {
            "start_idx": start_idx,
            "end_idx": end_idx,
            "noun_chunk": caption[start_idx:end_idx],
            "entity_tag": [entity_tag],
            "box_id": entity_tag,
        }
        entities.append(entity)

    return entities

class DataProcessor:
    def __init__(self, coco_entities_file, coco_images_root, save_path):
        self.coco_entities_file = coco_entities_file
        self.coco_images_root = coco_images_root
        self.save_path = save_path
        self.processed = {"train": [], "val": [], "test": [], "val_grouped": [], "test_grouped": []}
        self.stats = {"train": [], "val": [], "test": [], "val_grouped": [], "test_grouped": []}
        self.dropped_samples = []
    
    def read_coco_entities(self):
        logging.info(f"Loading CoCo Entities from {self.coco_entities_file}...")
        self.coco_entities = json.load(open(self.coco_entities_file, "r"))
        logging.info("Done.")

    def load_splits(self):
        """Load image_id (str) of "train", "val" and "test" splits
        """
        logging.info("Loading splits...")
        self.splits = {"train": [], "val": [], "test": []}
        for image_id, entities in self.coco_entities.items():
            split = list(entities.values())[0]["split"]
            self.splits[split].append(image_id)
        for split in ["train", "val", "test"]:
            logging.info(f"Loaded {len(self.splits[split])} {split} images.")
        logging.info("Done.")

    def load_image_name(self):
        """Find image name from image_id
        """
        logging.info(f"Matching image name from {self.coco_images_root}...")
        self.image = {}
        names = {
            "test2014": "COCO_test2014_{}.jpg",
            "test2015": "COCO_test2015_{}.jpg",
            "train2014": "COCO_train2014_{}.jpg",
            "val2014": "COCO_val2014_{}.jpg"
        }
        for image_id in tqdm(self.coco_entities.keys()):
            image_id_ = str(image_id).zfill(12)
            for folder, name in names.items():
                image_name = os.path.join(folder, name.format(image_id_))
                image_path = os.path.join(self.coco_images_root, image_name)
                if os.path.exists(image_path):
                    self.image[image_id] = image_name
                    break           
            if image_id not in self.image:     
                raise ValueError("Image name not found: {}".format(image_id))
        logging.info("Done.")

    def load_image_size(self):
        logging.info(f"Reading image size from {self.coco_images_root}...")
        self.image_size = {}
        for image_id, image_name in tqdm(self.image.items()):
            image_path = os.path.join(self.coco_images_root, image_name)
            image = Image.open(image_path)
            width, height = image.size
            depth = len(image.getbands())
            self.image_size[image_id] = [width, height, depth]
        logging.info("Done.")

    def load_boxes(self):
        logging.info(f"Loading boxes...")
        self.boxes = {}
        for image_id, annotations in tqdm(self.coco_entities.items()):
            boxes = {}
            for ann in annotations.values():
                for box_id, box in ann["detections"].items():
                    if box_id not in boxes:
                        # box = [[det_id ,[x_min, y_min, x_max, y_max]], ...]
                        boxes[box_id] = [b[1] for b in box]
            self.boxes[image_id] = boxes
        logging.info("Done.")

    def load_annotations(self):
        logging.info(f"Loading annotations...")
        self.annotations = {}   # {image_id: [{"caption": caption, "entities": entities}]}
        for image_id, annotations in tqdm(self.coco_entities.items()):
            anns = []
            for caption, ann in annotations.items():
                det_sequences = ann["det_sequences"]
                entities = get_entities(caption, det_sequences)
                anns.append({"caption": caption, "entities": entities})
            self.annotations[image_id] = anns
        logging.info("Done.")

    def process_examples(self):
        logging.info("Processing examples...") 
        self.examples = {}
        for image_id in tqdm(self.coco_entities.keys()):
            self.examples[image_id] = {}
            self.examples[image_id]["image_id"] = int(image_id)
            self.examples[image_id]["image"] = self.image[image_id]
            self.examples[image_id]["image_size"] = self.image_size[image_id]
            self.examples[image_id]["annotations"] = self.annotations[image_id]
            self.examples[image_id]["boxes"] = self.boxes[image_id]
        logging.info("Done.")

    def drop_no_box_entity(self, image_id, annotations):
        """Drop entities that have no box (e.g. "_", None)
        Args:
            image_id (str): the image_id of the annotations
            annotations (list): the extracted annotations from `load_entities`
        Returns:
            annotations (list, None): the annotations with filtered entities
                None, if none of the annotation has entity left
        """
        new_annotations = []
        for ann in annotations:
            entities = []
            for entity in ann["entities"]:
                if entity["box_id"] in self.boxes[image_id]:
                    entities.append(entity)
            if len(entities) > 0:
                new_ann = {"caption": ann["caption"], "entities": entities}
                new_annotations.append(new_ann)
        if len(new_annotations) > 0:
            return new_annotations
        else:
            self.dropped_samples.append(image_id)
            logging.debug(f"Image '{image_id}' has no annotation left.")
            return None
        
    def process_train(self, filter_no_box_entity=True):     
        """Process training samples
        Each sample consists of a image and a caption-entity pair.
        """
        logging.info("Processing train set...")   
        if filter_no_box_entity: 
            logging.info("Filter not box entity is enable.")
        image_num = 0
        for image_id in tqdm(self.splits["train"]):
            example = copy(self.examples[image_id])
            image = example["image"]
            image_id = example["image_id"]
            image_size = example["image_size"]
            annotations = example["annotations"]
            boxes = example["boxes"]
            # Drop the no box entity incide the annotations[{"entities"}]
            if filter_no_box_entity:
                annotations = self.drop_no_box_entity(str(image_id), annotations)
            if annotations is not None:
                image_num += 1
                # split annotations into samples
                for annotation in annotations:
                    example_ = {
                        "image_id": image_id,
                        "image": image,
                        "image_size": image_size,
                        "annotations": [annotation],
                        "boxes": boxes,
                    }
                    self.processed["train"].append(example_)
        sample_num = cap_num = len(self.processed["train"])
        self.stats["train"] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"# train [samples|images|caption]: [{sample_num}|{image_num}|{cap_num}]")

    def process_val(self, split="val", filter_no_box_entity=True):     
        """Process val/test samples
        Each sample consists of a image and mulit caption-entity pairs.
        """
        logging.info(f"Processing {split} set...")
        if filter_no_box_entity: 
            logging.info("Filter not box entity is enable.")
        cap_num = 0   
        for image_id in tqdm(self.splits[split]):
            example = copy(self.examples[image_id])
            image = example["image"]
            image_id = example["image_id"]
            image_size = example["image_size"]
            annotations = example["annotations"]
            boxes = example["boxes"]
            # Drop the no box entity incide the annotations[{"entities"}]
            if filter_no_box_entity:
                annotations = self.drop_no_box_entity(str(image_id), annotations)
            if annotations is not None:
                example_ = {
                    "image_id": image_id,
                    "image": image,
                    "image_size": image_size,
                    "annotations": annotations,
                    "boxes": boxes,
                }
                self.processed[split].append(example_)
                cap_num += len(annotations)
        sample_num = image_num = len(self.processed[split])
        self.stats[split] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"# {split} [samples|images|caption]: [{sample_num}|{image_num}|{cap_num}]")
    
    def process_val_grouped(self, split="test", filter_no_box_ann=True):
        """Process val/test samples into SCT style.
        Split and group the annotations with the same bbox sequence into samples.
        Each sample consists of a image and mulit caption-entity pairs **with the
        same bbox-sequence **.
            ref to the following link for details:
            https://github.com/aimagelab/show-control-and-tell/blob/master/test_region_sequence.py#L133
        """

        def drop_no_box_ann(image_id, annotations):
            """Drop annotations that have no box (e.g. "_")
            Args:
                image_id (str): the image_id of the annotations
                annotations (list): the extracted annotations from `load_entities`
            Returns:
                annotations (list, None): the filtered annotations
                    None, if none of the annotation has annotation left
            """
            new_annotations = []
            for ann in annotations:
                # skip the annotations that contains no box ("_") entities
                if "_" in [entity["box_id"] for entity in ann["entities"]]:
                    continue
                new_annotations.append(ann)
            new_annotations = self.drop_no_box_entity(image_id, new_annotations)
            return new_annotations
        
        def find_unique_sublists(lst):
            unique_sublists, unique_indexes, unique_inverse = [], [], []
            for i, sublist in enumerate(lst):
                if sublist not in unique_sublists:
                    unique_indexes.append(i)
                    unique_sublists.append(sublist)
                unique_inverse.append(unique_sublists.index(sublist))
            return unique_indexes, unique_inverse
        
        logging.info(f"Processing {split}_grouped set...")
        if filter_no_box_ann:
            logging.info("Filter not box annotations is enable.")
        image_num, cap_num = 0, 0
        for image_id in tqdm(self.splits[split]):
            example = copy(self.examples[image_id])
            image = example["image"]
            image_id = example["image_id"]
            image_size = example["image_size"]
            annotations = example["annotations"]
            boxes = example["boxes"]
            # Drop annotations that contain no box entities(e.g. "_")
            if filter_no_box_ann:
                annotations = drop_no_box_ann(str(image_id), annotations)
            if annotations is not None:
                image_num += 1
                cap_num += len(annotations)
                # Group annotations with the same bbox sequence into samples
                box_seq_list = []
                for ann in annotations:
                    # use box_id to identify the bbox sequence
                    box_seq = [item["box_id"] for item in ann["entities"]]
                    box_seq_list.append(box_seq)
                unique_indexes, unique_inverse = find_unique_sublists(box_seq_list)
                unique_inverse = np.array(unique_inverse)   # to use np.where
                for uni_idx in unique_indexes:
                    annotations_ = [annotations[idx] for idx in np.where(unique_inverse==uni_idx)[0]]
                    example_ = {
                        "image_id": image_id,
                        "image": image,
                        "image_size": image_size,
                        "annotations": annotations_,
                        "boxes": boxes,
                    }
                    self.processed[f"{split}_grouped"].append(example_)

        sample_num = len(self.processed[f"{split}_grouped"])
        self.stats[f"{split}_grouped"] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"# {split}_grouped [samples|images|caption]: [{sample_num}|{image_num}|{cap_num}]")

    def save_to_disk(self):
        logging.info("Saving to disk...")
        file_name = {
            "train": "train.json",
            "val": "val.json",
            "test": "test.json",
            "val_grouped": "val_grouped.json",
            "test_grouped": "test_grouped.json",
            "info": "info.json",
        }
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        for split in ["train", "val", "test", "val_grouped", "test_grouped"]:
            logging.info(f"Saving {split} set...")
            save_path = os.path.join(self.save_path, file_name[split])
            json.dump(self.processed[split], open(save_path, "w"))
            logging.info(f"Saved {split} set to {save_path}")
        save_path = os.path.join(self.save_path, file_name["info"])
        json.dump(self.stats, open(save_path, "w"))
        logging.info(f"Saved info to {save_path}")
        print("Stats:", self.stats)

import argparse
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--coco_entities_file", type=str, required=True)
    argparser.add_argument("--coco_images_root", type=str, required=True)
    argparser.add_argument("--save_path", type=str, default="./")
    args = argparser.parse_args()
    
    processor = DataProcessor(args.coco_entities_file, args.coco_images_root, args.save_path)
    processor.read_coco_entities()
    processor.load_splits()         # self.splits = {"train": [image_id], "val": [image_id], "test": [image_id]}
    processor.load_image_name()     # self.image = {image_id: image_name}
    processor.load_image_size()     # self.image_size = {image_id: [width, height, depth]}
    processor.load_boxes()          # self.boxes = {image_id: {box_id: [x_min, y_min, x_max, y_max]}}
    processor.load_annotations()    # self.annotations = {image_id: [{"caption": caption, "entities": entities}]}    
    processor.process_examples()    # self.examples = {"image_id", "image", "image_size", "annotations", "boxes"}
    processor.process_train(filter_no_box_entity=True)
    processor.process_val(split="val", filter_no_box_entity=True)
    processor.process_val(split="test", filter_no_box_entity=True)
    processor.process_val_grouped(split="val", filter_no_box_ann=True)
    processor.process_val_grouped(split="test", filter_no_box_ann=True)
    processor.save_to_disk()
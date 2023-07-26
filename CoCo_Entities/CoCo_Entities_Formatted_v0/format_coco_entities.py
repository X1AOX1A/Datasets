import os
import sys
import json
import numpy as np

try:
    from loguru import logger as logging
    logging.add(sys.stderr, filter="my_module")
except ImportError:
    import logging

class DataProcessor:
    def __init__(self, coco_entities_file, coco_images_root, save_path):
        self.coco_entities_file = coco_entities_file
        self.coco_images_root = coco_images_root
        self.save_path = save_path
        self.processed = {"train": [], "val": [], "test": [], "test_sct": []}
        self.stats = {"train": {}, "val": {}, "test": {}, "test_sct": {}}
    
    def read_coco_entities(self):
        logging.info("Loading CoCo Entities...")
        self.coco_entities = json.load(open(self.coco_entities_file, "r"))
        logging.info("Done.")

    def into_split(self):
        self.coco_entities_splits = {"train": {}, "val": {}, "test": {}}
        for image_id, entities in self.coco_entities.items():
            split = list(entities.values())[0]["split"]
            self.coco_entities_splits[split][image_id] = entities

    def find_image_name(self, image_id: int):
        image_id_ = str(image_id).zfill(12)
        names = {
            "test2014": "COCO_test2014_{}.jpg",
            "test2015": "COCO_test2015_{}.jpg",
            "train2014": "COCO_train2014_{}.jpg",
            "val2014": "COCO_val2014_{}.jpg"
        }
        for folder, name in names.items():
            image_name = os.path.join(folder, name.format(image_id_))
            image_path = os.path.join(self.coco_images_root, image_name)
            if os.path.exists(image_path):
                return image_name
        raise ValueError("image_id {} not found".format(image_id))

    def get_entity_start_end_indices(self, caption, det_sequences):
        """Get the start and end indices of entities in the caption
        Args:
            caption (str): the caption of CoCo Entities, 
                e.g. "a woman and man sits on a wooden bench"
            det_sequences (list): list of entity tags, 
                e.g. ['woman', 'woman', None, 'man', None, None, 'bench', 'bench', 'bench']
        Returns:
            entity_start_end_indices (list): [[start_idx, end_idx, entity_tag]]
                e.g. [[0, 7], [12, 15], [24, 38]]
        """
        off_set, prev_end_idx = 0, 0
        prev_entity = None
        entity_start_end_indices = []
        caption_word = caption.split(" ")
        assert len(caption_word) == len(det_sequences)
        for i, (word, entity) in enumerate(zip(caption_word, det_sequences)):
            if entity == prev_entity:
                end_idx = len(word) if i==0 else min(prev_end_idx+len(word)+1, len(caption))
                if entity not in [None, "_"]:
                    entity_start_end_indices[-1][1] = end_idx
            else:
                start_idx = off_set
                end_idx = start_idx + len(word)
                if entity not in [None, "_"]:
                    entity_start_end_indices.append([start_idx, end_idx])
                prev_entity = entity
            off_set = end_idx+1
            prev_end_idx = end_idx

        return entity_start_end_indices
    
    def extract_entity_chunks(self, caption, entities):
        """Extract noun chunks from CoCo Entities
        Args: 
            caption (str): the caption of CoCo Entities
            entities (dict): with keys "det_sequences", "noun_chunks", "detections", 
                ref to the following link for details:
                https://github.com/aimagelab/show-control-and-tell/tree/master#coco-entities-1
        Returns:
            entity_chunks (list): [[start_idx, end_idx, x1, y1, x2, y2, entity_tag]]
                start_idx, end_idx (int): closed, opened
                x1, y1, x2, y2 (float): bbox coordinates of upper left and lower right corners
                entity_tag (str): optioal, not used so far, entity tag of the entity chunk
        """
        det_sequences = entities["det_sequences"]
        noun_chunks = {item[0]: item[1] for item in entities["noun_chunks"]}
        entity_start_end_indices = self.get_entity_start_end_indices(caption, det_sequences)
        entity_chunks = []
        entity_set = set()
        for start_idx, end_idx in entity_start_end_indices:
            entity_tag = noun_chunks[caption[start_idx:end_idx]]
            if entity_tag not in entity_set:
                entity_set.add(entity_tag)
                x1, y1, x2, y2 = entities["detections"][entity_tag][0][1]
                entity_chunks.append([start_idx, end_idx, x1, y1, x2, y2, entity_tag])

        entity_chunks = sorted(entity_chunks, key=lambda x: x[0])
        # assert not overleapping and start_idx < end_idx
        for i in range(len(entity_chunks)):
            if i == 0:
                continue
            assert entity_chunks[i][0] >= entity_chunks[i-1][1]        
        return entity_chunks
        
    def process_train(self):
        """Process training samples
        Each sample consists of a image and a caption-entity pair.
        """
        logging.info("Processing train set...")
        for image_id, ann in self.coco_entities_splits["train"].items():
            image_id = int(image_id)
            image_name = self.find_image_name(image_id)
            for caption, entities in ann.items():
                entity_chunks = self.extract_entity_chunks(caption, entities)
                example = {
                    "image": image_name,
                    "image_id": image_id,
                    "annotations":[
                        {
                            "caption": caption,
                            "entity": entity_chunks,
                        }
                    ]
                }
                self.processed["train"].append(example)
        sample_num = cap_num = len(self.processed["train"])
        image_num = len(set(self.coco_entities_splits["train"].keys()))    
        self.stats["train"] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"{sample_num} train samples processed.")
        logging.info(f"# of train [images|caption]: [{image_num}|{cap_num}]")

    def process_val(self, split="val"):
        """Process val/test samples
        Each sample consists of a image and mulit caption-entity pairs.
        """
        logging.info("Processing {} set...".format(split))
        cap_num = 0
        for image_id, ann in self.coco_entities_splits[split].items():
            image_id = int(image_id)
            image_name = self.find_image_name(image_id)
            annotations = []
            for caption, entities in ann.items():
                entity_chunks = self.extract_entity_chunks(caption, entities)
                annotations.append(
                    {
                        "caption": caption,
                        "entity": entity_chunks
                    }
                )
                cap_num += 1
            example = {
                "image": image_name,
                "image_id": image_id,
                "annotations": annotations,
            }
            self.processed[split].append(example)
        sample_num = len(self.processed[split])
        image_num = len(set(self.coco_entities_splits[split].keys()))        
        self.stats[split] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"{sample_num} {split} samples processed.")
        logging.info(f"# of {split} [images|captions]: [{image_num}|{cap_num}]")
    
    def process_test_sct(self, filtering=True):
        """Process test samples into SCT style.
        Each sample consists of a image and mulit caption-entity pairs **with the
        same entity tag chunks**.
            ref to the following link for details:
            https://github.com/aimagelab/show-control-and-tell/blob/923462105e99a422c2a47467700c779b90bf50a4/data/dataset.py#L72
        """
        logging.info("Processing test set into SCT format...")       
        test_sct_formatted = []
        cap_num = 0
        image_num = set()

        # process and filter test set (skip if "_" in entity_tags)
        for image_id, ann in self.coco_entities_splits["test"].items():
            image_id = int(image_id)
            image_name = self.find_image_name(image_id)
            annotations = []
            for caption, entities in ann.items():
                entity_tags = [item[1] for item in entities["noun_chunks"]]
                # skip if filtering and "_" in entity_tags
                if filtering and "_" in entity_tags: 
                    continue
                # else, extract entity chunks
                entity_chunks = self.extract_entity_chunks(caption, entities)
                annotations.append(
                    {
                        "caption": caption,
                        "entity": entity_chunks
                    }
                )
                cap_num += 1
            example = {
                "image": image_name,
                "image_id": image_id,
                "annotations": annotations,
            }
            if len(annotations) > 0:
                test_sct_formatted.append(example)
                image_num.add(image_id)

        def find_unique_sublists(lst):
            unique_sublists, unique_indexes, unique_inverse = [], [], []
            for i, sublist in enumerate(lst):
                if sublist not in unique_sublists:
                    unique_indexes.append(i)
                    unique_sublists.append(sublist)
                unique_inverse.append(unique_sublists.index(sublist))
            return unique_indexes, unique_inverse

        # group by entity tags list
        for example in test_sct_formatted:
            image = example["image"]
            image_id = example["image_id"]
            annotations = example["annotations"]
            entity_tags_list = []
            for ann in annotations:
                entity_tags = [item[6] for item in ann["entity"]]
                entity_tags_list.append(entity_tags)
            unique_indexes, unique_inverse = find_unique_sublists(entity_tags_list)
            unique_inverse = np.array(unique_inverse)   # to use np.where
            for uni_idx in unique_indexes:
                annotations_ = [annotations[idx] for idx in np.where(unique_inverse==uni_idx)[0]]
                example_ = {
                    "image": image,
                    "image_id": image_id,
                    "annotations": annotations_,
                }
                self.processed["test_sct"].append(example_)
                
        sample_num = len(self.processed["test_sct"])
        image_num = len(image_num)
        self.stats["test_sct"] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"{sample_num} test_sct samples processed.")
        logging.info(f"# of test_sct [images|captions]: [{image_num}|{cap_num}]")

    def save_to_disk(self):
        logging.info("Saving to disk...")
        file_name = {
            "train": "train.json",
            "val": "val.json",
            "test": "test.json",
            "test_sct": "test_sct.json",
            "info": "info.json",
        }
        for split in ["train", "val", "test", "test_sct"]:
            logging.info(f"Saving {split} set...")
            save_path = os.path.join(self.save_path, file_name[split])
            json.dump(self.processed[split], open(save_path, "w"))
            logging.info(f"Saved {split} set to {save_path}")
        save_path = os.path.join(self.save_path, file_name["info"])
        json.dump(self.stats, open(save_path, "w"))
        logging.info(f"Saved info to {save_path}")
        print("Stats:", self.stats)
        a = 1

import argparse
if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--coco_entities_file", type=str, required=True)
    argparser.add_argument("--coco_images_root", type=str, required=True)
    argparser.add_argument("--save_path", type=str, default="./")
    args = argparser.parse_args()
    
    processor = DataProcessor(args.coco_entities_file, args.coco_images_root, args.save_path)
    processor.read_coco_entities()
    processor.into_split()
    processor.process_train()
    processor.process_val(split="val")
    processor.process_val(split="test")
    processor.process_test_sct(filtering=True)
    processor.save_to_disk()
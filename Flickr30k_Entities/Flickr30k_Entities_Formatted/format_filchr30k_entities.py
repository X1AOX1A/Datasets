import os
import sys
import json
import numpy as np
from tqdm import tqdm
import xml.etree.ElementTree as ET
from copy import deepcopy as copy

try:
    from loguru import logger as logging
    logging.add(sys.stderr, filter="my_module")
except ImportError:
    import logging

import xml.etree.ElementTree as ET

def get_sentence_data(fn):
    """
    Parses a sentence file from the Flickr30K Entities dataset

    input:
      fn - full file path to the sentence file to parse
    
    output:
      a list of dictionaries for each sentence with the following fields:
          sentence - the original sentence
          phrases - a list of dictionaries for each phrase with the
                    following fields:
                      phrase - the text of the annotated phrase
                      first_word_index - the position of the first word of
                                         the phrase in the sentence
                      phrase_id - an identifier for this phrase
                      phrase_type - a list of the coarse categories this 
                                    phrase belongs to

    """
    with open(fn, 'r') as f:
        sentences = f.read().split('\n')

    annotations = []
    for sentence in sentences:
        if not sentence:
            continue

        first_word = []
        phrases = []
        phrase_id = []
        phrase_type = []
        words = []
        current_phrase = []
        add_to_phrase = False
        for token in sentence.split():
            if add_to_phrase:
                if token[-1] == ']':
                    add_to_phrase = False
                    token = token[:-1]
                    current_phrase.append(token)
                    phrases.append(' '.join(current_phrase))
                    current_phrase = []
                else:
                    current_phrase.append(token)

                words.append(token)
            else:
                if token[0] == '[':
                    add_to_phrase = True
                    first_word.append(len(words))
                    parts = token.split('/')
                    phrase_id.append(parts[1][3:])
                    phrase_type.append(parts[2:])
                else:
                    words.append(token)

        sentence_data = {'caption' : ' '.join(words), 'entities' : []}
        for index, phrase, p_id, p_type in zip(first_word, phrases, phrase_id, phrase_type):
            start_idx = 0 if index == 0 else len(" ".join(sentence_data["caption"].split(" ")[:index]))+1
            end_idx = start_idx + len(phrase)
            assert phrase == sentence_data["caption"][start_idx:end_idx]
            sentence_data['entities'].append({'start_idx' : start_idx,
                                             'end_idx' : end_idx,
                                             'noun_chunk' : phrase,
                                             'entity_tag' : p_type,
                                             'box_id' : p_id})

        annotations.append(sentence_data)

    return annotations

def get_annotations(fn):
    """
    Parses the xml files in the Flickr30K Entities dataset

    input:
      fn - full file path to the annotations file to parse

    output:
      dictionary with the following fields:
        filename - the name of the file
          scene - list of identifiers which were annotated as
                  pertaining to the whole scene
          nobox - list of identifiers which were annotated as
                  not being visible in the image
          boxes - a dictionary where the fields are identifiers
                  and the values are its list of boxes in the 
                  [xmin ymin xmax ymax] format
    """
    tree = ET.parse(fn)
    root = tree.getroot()
    size_container = root.findall('size')[0]
    anno_info = {'filename' : root.findall('filename')[0].text, 'scene' : [], 'nobox' : [], 'boxes' : {}}
    for size_element in size_container:
        anno_info[size_element.tag] = int(size_element.text)

    for object_container in root.findall('object'):
        for names in object_container.findall('name'):
            box_id = names.text
            box_container = object_container.findall('bndbox')
            if len(box_container) > 0:
                if box_id not in anno_info['boxes']:
                    anno_info['boxes'][box_id] = []
                xmin = int(box_container[0].findall('xmin')[0].text) - 1
                ymin = int(box_container[0].findall('ymin')[0].text) - 1
                xmax = int(box_container[0].findall('xmax')[0].text) - 1
                ymax = int(box_container[0].findall('ymax')[0].text) - 1
                anno_info['boxes'][box_id].append([xmin, ymin, xmax, ymax])
            else:
                nobndbox = int(object_container.findall('nobndbox')[0].text)
                if nobndbox > 0:
                    anno_info['nobox'].append(box_id)

                scene = int(object_container.findall('scene')[0].text)
                if scene > 0:
                    anno_info['scene'].append(box_id)
    return anno_info

class DataProcessor:
    def __init__(self, flickr_entities_root, flickr_images_root, save_path):
        self.flickr_entities_root = flickr_entities_root
        self.flickr_images_root = flickr_images_root
        self.save_path = save_path
        self.processed = {"train": [], "val": [], "test": [], "val_grouped": [], "test_grouped": []}
        self.stats = {"train": [], "val": [], "test": [], "val_grouped": [], "test_grouped": []}
        self.dropped_samples = []
    
    def load_splits(self):
        """Load image_id (str) of "train", "val" and "test" splits
        """
        splits = {
            "train": "train.txt",
            "val": "val.txt",
            "test": "test.txt",
        }
        self.splits = {}
        for split, split_file in splits.items():
            file_path = os.path.join(self.flickr_entities_root, split_file)
            logging.info(f"Loading {split} image ids from {file_path} ...") 
            with open(file_path, "r") as f:
                self.splits[split] = [line.strip() for line in f.readlines()]
                assert len(self.splits[split]) == len(set(self.splits[split]))
                logging.info(f"Loaded {len(self.splits[split])} {split} images.")
        logging.info("Done.")

    def load_annotations(self):
        annotations_path = os.path.join(self.flickr_entities_root, "Annotations")
        logging.info(f"Loading annotations from {annotations_path}...") 
        self.image = {}
        self.image_size = {}
        self.boxes = {}
        for file in tqdm(os.listdir(annotations_path)):
            ann_path = os.path.join(annotations_path, file)
            image_id = file.split(".")[0]   # str
            annotation = get_annotations(ann_path)
            self.image[image_id] = annotation["filename"]
            self.image_size[image_id] = [annotation["width"], annotation["height"], annotation["depth"]]
            self.boxes[image_id] = annotation["boxes"]
        logging.info("Done.")

    def load_sentences(self):
        """Load sentences of all images
        """
        sentences_path = os.path.join(self.flickr_entities_root, "Sentences")
        logging.info(f"Loading sentences from {sentences_path}...") 
        self.annotations = {}
        # read all txt files in the folder, with file name as the key and content as the value
        for file in tqdm(os.listdir(sentences_path)):
            annotations = get_sentence_data(os.path.join(sentences_path, file))
            image_id = file.split(".")[0]            
            self.annotations[image_id] = annotations
        logging.info("Done.")
    
    def process_examples(self):
        logging.info("Processing examples...") 
        self.examples = {}
        for image_id in tqdm(self.annotations.keys()):
            self.examples[image_id] = {}
            self.examples[image_id]["image_id"] = int(image_id)
            self.examples[image_id]["image"] = self.image[image_id]
            self.examples[image_id]["image_size"] = self.image_size[image_id]
            self.examples[image_id]["annotations"] = self.annotations[image_id]
            self.examples[image_id]["boxes"] = self.boxes[image_id]
        logging.info("Done.")

    def drop_no_box_entity(self, image_id, annotations):
        """Drop entities that have no box (e.g. no_box, scene)
        Args:
            image_id (str): the image_id of the annotations
            annotations (list): the extracted annotations from `get_sentence_data`
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
            annotations = example["annotations"]
            # Drop the no box entity incide the annotations[{"entities"}]
            if filter_no_box_entity:
                annotations = self.drop_no_box_entity(image_id, annotations)
            if annotations is not None:
                image_num += 1
                # split annotations into samples
                for annotation in annotations:
                    sample = example
                    sample["annotations"] = [annotation]
                    self.processed["train"].append(sample)
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
            annotations = example["annotations"]
            # Drop the no box entity incide the annotations[{"entities"}]
            if filter_no_box_entity:
                annotations = self.drop_no_box_entity(image_id, annotations)
            if annotations is not None:
                sample = example
                sample["annotations"] = annotations
                self.processed[split].append(sample)
                cap_num += len(annotations)
        sample_num = image_num = len(self.processed[split])
        self.stats[split] = {"sample_num": sample_num, "image_num": image_num, "cap_num": cap_num}
        logging.info(f"# {split} [samples|images|caption]: [{sample_num}|{image_num}|{cap_num}]")
    
    def process_val_grouped(self, split="test", filter_no_box_entity=True):
        """Process val/test samples into SCT style.
        Split and group the annotations with the same bbox sequence into samples.
        Each sample consists of a image and mulit caption-entity pairs **with the
        same bbox-sequence **.
            ref to the following link for details:
            https://github.com/aimagelab/show-control-and-tell/blob/master/test_region_sequence.py#L133
        """
        
        def find_unique_sublists(lst):
            unique_sublists, unique_indexes, unique_inverse = [], [], []
            for i, sublist in enumerate(lst):
                if sublist not in unique_sublists:
                    unique_indexes.append(i)
                    unique_sublists.append(sublist)
                unique_inverse.append(unique_sublists.index(sublist))
            return unique_indexes, unique_inverse
        
        logging.info(f"Processing {split}_grouped set...")
        if filter_no_box_entity: 
            logging.info("Filter not box entity is enable.")
        image_num, cap_num = 0, 0
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
                image_num += 1
                cap_num += len(annotations)
                # Split annotations with the same bbox sequence into samples
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


if __name__ == "__main__":
    flickr_entities_root = "/root/Documents/DATASETS/Flickr30k_Entities"
    flickr_images_root = "/root/Documents/DATASETS/Flickr30k/images"
    save_path = "/root/Documents/DATASETS/Flickr30k_Entities/Flickr30k_Entities_Formatted/annotations"
    processor = DataProcessor(flickr_entities_root, flickr_images_root, save_path)
    processor.load_splits()
    processor.load_annotations()
    processor.load_sentences()
    processor.process_examples()
    processor.process_train(filter_no_box_entity=True)
    processor.process_val("val", filter_no_box_entity=True)
    processor.process_val("test", filter_no_box_entity=True)
    processor.process_val_grouped(split="val", filter_no_box_entity=True)
    processor.process_val_grouped(split="test", filter_no_box_entity=True)
    processor.save_to_disk()
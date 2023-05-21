# pip install tfrecord
# Add `default value ""` to tfrecord.reader.process_feature
# tfrecord/reader.py/line 116
#         value = value[0] if value else ""

import torch
import os
from pprint import pprint as print
from tfrecord.torch.dataset import TFRecordDataset

def WikiWeb2M_dataset(data_dir, split):
    """
    Args:
        data_dir: path to the directory containing the tfrecord files and index files
            the tfrecord files are named as "wikiweb2m-{split}.tfrecord"
            the index files are named as "wikiweb2m-{split}.tfidnex"
        split: one of "train", "val", "test"
    Returns:
        dataset: a TFRecordDataset object
    """

    tfrecord_path = os.path.join(data_dir, f"wikiweb2m-{split}.tfrecord")
    index_path = os.path.join(data_dir, f"wikiweb2m-{split}.tfidnex")

    context_description = {
        "split": "byte",
        "page_title": "byte",
        "page_url": "byte",
        "clean_page_description": "byte",
        "raw_page_description": "byte",
        "is_page_description_sample": "int",
        "page_contains_images": "int",
        "page_content_sections_without_table_list": "int"
    }

    sequence_description = {
        "is_section_summarization_sample": "int",
        "section_title": "byte",
        "section_index": "int",
        "section_depth": "int",
        "section_heading_level": "int",
        "section_subsection_index": "int",
        "section_parent_index": "int",
        "section_text": "byte",
        "section_clean_1st_sentence": "byte",
        "section_raw_1st_sentence": "byte",
        "section_rest_sentence": "byte",
        "is_image_caption_sample": "int",
        "section_image_url": "byte",
        "section_image_mime_type": "byte",
        "section_image_width": "int",
        "section_image_height": "int",
        "section_image_in_wit": "int",
        "section_contains_table_or_list": "int",
        "section_image_captions": "byte",
        "section_image_alt_text": "byte",
        "section_image_raw_attr_desc": "byte",
        "section_image_clean_attr_desc": "byte",
        "section_image_raw_ref_desc": "byte",
        "section_image_clean_ref_desc": "byte",
        "section_contains_images": "int"
    }

    dataset = TFRecordDataset(
        data_path=tfrecord_path, 
        index_path=index_path, 
        description=context_description,
        sequence_description=sequence_description
    )

    return dataset

if __name__ == "__main__":
    DATA_DIR = "/data/root/Documents/DATASETS/WikiWeb2M"

    split = "train"
    batch_size = 1
    dataset = WikiWeb2M_dataset(DATA_DIR, split)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)
    data = next(iter(dataloader))
    print(data)
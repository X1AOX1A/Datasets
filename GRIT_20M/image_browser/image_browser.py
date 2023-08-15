try:
    from loguru import logger as logging
    import sys
    logging.add(sys.stderr, filter="my_module")
except ImportError:
    import logging

import os  
import json
import requests  
from urllib.parse import urlparse  
import textwrap

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 20, 12
import cv2
import random
from PIL import Image
import streamlit as st

@st.cache_data
def read_jsons(file_name: str, sample_num: int = None):
    dict_objs = []
    count = 0
    logging.info(f"Reading {sample_num }samples from {file_name}...")
    with open(file_name, "r") as f:
        for line in f:
            dict_objs.append(json.loads(line))
            count += 1
            if sample_num is not None and count >= sample_num:
                break
    logging.info(f"Read {count} samples from {file_name}")
    return dict_objs

@st.cache_data
def get_image_url_dict(image_url_to_path):
    logging.info("Loading image url to path dict...")
    with open(image_url_to_path, "r") as f:
        dict_objs = json.load(f)
    logging.info(f"Loaded {len(dict_objs)} image url to path mappings")
    return dict_objs

def get_image_path(annotation, tmp_dir="./tmp", image_url_dict=None):
    """Get image path from annotation. If image is not downloaded yet, download it.
    Args:
        annotation: dict, annotation of an image read from jsonl
        tmp_dir: str, path to tmp dir
        image_url_to_path: dict, mapping from image url to image path
    Returns:
        image_path: str, path to image
    """
    url = annotation['url']

    # check if image is already downloaded
    if image_url_dict is not None and url in image_url_dict:
        image_path = image_url_dict[url]
        if os.path.exists(image_path):
            logging.info(f"Image {url} already downloaded")
            st.info(f"Image {url} already downloaded")
            return image_path
        else:
            logging.warning(f"Image {url} not found at local path")

    # try to download image
    try:  
        logging.info(f"Downloading {url}...")
        st.info(f"Downloading {url}...")
        response = requests.get(url)  
        response.raise_for_status()              
        file_name = os.path.basename(urlparse(url).path)  
        file_key_name = annotation['key'] + os.path.splitext(file_name)[1]
        image_path = os.path.join(tmp_dir, file_key_name)             
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    except Exception as e:  
        logging.error(f"Error while downloading {url}: {e}")
        st.error(f"Error while downloading {url}: {e}")
        return None


def draw_annotation(annotation, image_path, tmp_dir="./tmp"):
    try:
        pil_img = Image.open(image_path).convert("RGB")
    except Exception as e:
        logging.error(f"Error while opening image {image_path}: {e}")
        st.error(f"Error while opening image {image_path}: {e}")
        return None
    image = np.array(pil_img)[:, :, [2, 1, 0]]
    image_h = pil_img.height
    image_w = pil_img.width
    caption = annotation['caption']
    
    def is_overlapping(rect1, rect2):  
        x1, y1, x2, y2 = rect1  
        x3, y3, x4, y4 = rect2  
        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4) 
    
    grounding_list = annotation['ref_exps']
    new_image = image.copy()
    previous_locations = []
    previous_bboxes = []
    text_offset = 10
    text_offset_original = 4
    text_size = max(0.07 * min(image_h, image_w) / 100, 0.5)
    text_line = int(max(1 * min(image_h, image_w) / 512, 1))
    box_line = int(max(2 * min(image_h, image_w) / 512, 2))
    text_height = text_offset # init
    # pdb.set_trace()
    for (phrase_s, phrase_e, x1_norm, y1_norm, x2_norm, y2_norm, score) in grounding_list:  
        phrase = caption[phrase_s:phrase_e]
        x1, y1, x2, y2 = int(x1_norm * image_w), int(y1_norm * image_h), int(x2_norm * image_w), int(y2_norm * image_h)
        print(f"Decode results: {phrase} - {[x1, y1, x2, y2]}")
        st.info(f"Decode results: {phrase} - {[x1, y1, x2, y2]}")
        # draw bbox
        # random color
        color = tuple(np.random.randint(0, 255, size=3).tolist())
        new_image = cv2.rectangle(new_image, (x1, y1), (x2, y2), color, box_line)
        
        # add phrase name  
        # decide the text location first  
        for x_prev, y_prev in previous_locations:  
            if abs(x1 - x_prev) < abs(text_offset) and abs(y1 - y_prev) < abs(text_offset):  
                y1 += text_height  

        if y1 < 2 * text_offset:  
            y1 += text_offset + text_offset_original  

        # add text background
        (text_width, text_height), _ = cv2.getTextSize(phrase, cv2.FONT_HERSHEY_SIMPLEX, text_size, text_line)  
        text_bg_x1, text_bg_y1, text_bg_x2, text_bg_y2 = x1, y1 - text_height - text_offset_original, x1 + text_width, y1  
        
        for prev_bbox in previous_bboxes:  
            while is_overlapping((text_bg_x1, text_bg_y1, text_bg_x2, text_bg_y2), prev_bbox):  
                text_bg_y1 += text_offset  
                text_bg_y2 += text_offset  
                y1 += text_offset 
                
                if text_bg_y2 >= image_h:  
                    text_bg_y1 = max(0, image_h - text_height - text_offset_original)  
                    text_bg_y2 = image_h  
                    y1 = max(0, image_h - text_height - text_offset_original + text_offset)  
                    break 
        
        alpha = 0.5  
        for i in range(text_bg_y1, text_bg_y2):  
            for j in range(text_bg_x1, text_bg_x2):  
                if i < image_h and j < image_w: 
                    new_image[i, j] = (alpha * new_image[i, j] + (1 - alpha) * np.array(color)).astype(np.uint8) 
        
        cv2.putText(  
            new_image, phrase, (x1, y1 - text_offset_original), cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 0), text_line, cv2.LINE_AA  
        )  
        previous_locations.append((x1, y1))  
        previous_bboxes.append((text_bg_x1, text_bg_y1, text_bg_x2, text_bg_y2))
    
    try:
        file_key_name = annotation['key'] + '_anno' + os.path.splitext(image_path)[1]
        anno_image_path = os.path.join(tmp_dir, file_key_name)        
        save_annotated_image(new_image, file_name=anno_image_path, caption=caption)
        return anno_image_path
    except Exception as e:
        logging.error(f"Error while saving {image_path}: {e}")
        st.error(f"Error while saving {image_path}: {e}")
        # Out of (supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp)
        return None

def save_annotated_image(img, file_name="tmp.jpg", caption='test'):
    # Create figure and axis objects
    fig, ax = plt.subplots()
    # Show image on axis
    ax.imshow(img[:, :, [2, 1, 0]])
    ax.set_axis_off()
    # Set caption text
    # Add caption below image
    if caption:
        st.info("Caption: " + caption)
        ax.text(0.5, -0.2, '\n'.join(textwrap.wrap(caption, 120)), ha='center', transform=ax.transAxes, fontsize=18)
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()

def main(args):
    # st.set_page_config(layout="wide")
    st.title("Image Browser")    
    annotations = read_jsons(args.path_to_ann, args.sample_num)    
    image_url_dict = get_image_url_dict(args.image_url_to_path) if args.image_url_to_path else None

    # Create radio buttons to select the index or choose random
    sample_idx = st.text_input(f"Enter an index between [0, {args.sample_num-1}] or type 'Random'", value="0")

    if sample_idx != "":
        if sample_idx in ["Random", "random"]:
            sample_idx = random.randint(0, args.sample_num)
            logging.info(f"Randomly selected index: {sample_idx}")
            st.info(f"Randomly selected index: {sample_idx}")
        else:
            sample_idx = int(sample_idx)

        # Get image paths based on selected index
        image_path = get_image_path(annotations[sample_idx], args.tmp_dir, image_url_dict)
        anno_image_path = draw_annotation(annotations[sample_idx], image_path, args.tmp_dir)

        if image_path and anno_image_path:
            # Display images
            col1, col2 = st.columns(2)
            with col1:
                st.write("Original Image")
                image = Image.open(image_path)
                st.image(image, caption='Original Image', use_column_width="auto", )
            with col2:
                st.write("Annotated Image")
                anno_image = Image.open(anno_image_path)
                st.image(anno_image, caption='Annotated Image', use_column_width="auto")
        else:
            st.warning("Invalid index or no images found for the selected index.")

# class args:
#     path_to_ann = "/root/Documents/DATASETS/GRIT_20M/download/grit_coyo.jsonl"
#     image_url_to_path = "/root/Documents/DATASETS/GRIT_20M/download/image_url_to_path.json"
#     tmp_dir = "/root/Documents/DATASETS/GRIT_20M/tmp"
#     sample_num = 1000

import argparse
def args_parser():
    parser = argparse.ArgumentParser(description='Image Browser')
    parser.add_argument('--path_to_ann', type=str, help='Path to the annotation file.')
    parser.add_argument('--image_url_to_path', type=str, default=None, help='Path to the image url to path file. If not provided, the image path will be downloaded each time requested.')
    parser.add_argument('--tmp_dir', type=str, default="./tmp", help='Path to the tmp directory.')
    parser.add_argument('--sample_num', type=int, default=1000,help='Number of samples to display.')
    return parser.parse_args()

if __name__ == "__main__":
    args = args_parser()
    main(args)
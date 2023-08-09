import os
import json
from tqdm import tqdm

def extract_image_url_to_path(image_root):
    image_url_to_path = {}
    dumplicate_image_num = 0
    dirs= list(os.walk(image_root).__next__()[1])   # ["_tmp", "00000", "000001", "..."]
    for dir in tqdm(dirs):    
        for _, _, files in os.walk(os.path.join(image_root, dir)):    # 
            for file in files:
                if file.endswith(".jpg"):            
                    try:
                        info_file = file.replace(".jpg", ".json")
                        url = read_json(os.path.join(image_root, dir, info_file))["url"]
                        if url in image_url_to_path:
                            dumplicate_image_num += 1
                        else:
                            image_url_to_path[url] = os.path.join(image_root, dir, file)
                    except Exception as e:
                        print(e)
                        continue
    print(f"Processed {len(image_url_to_path)+dumplicate_image_num} images.")
    print(f"{dumplicate_image_num} dumplicate images (url) skipped.")
    print(f"Extracted {len(image_url_to_path)} image paths.")
    return image_url_to_path

def read_json(file_name: str):
    with open(file_name, "r") as f:
        dict_objs = json.load(f)
    return dict_objs

def write_json(dict_objs, file_name: str):
    print(f"Writing json file to {file_name}...")
    with open(file_name, "w+") as f:
        json.dump(dict_objs, f, ensure_ascii=False)

import argparse
if __name__ == '__main__':  
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_root', type=str, default='./download/images')
    parser.add_argument('--image_url_to_path', type=str, default='./download/image_url_to_path.json')
    args = parser.parse_args()
    image_url_to_path = extract_image_url_to_path(args.image_root)
    write_json(image_url_to_path, args.image_url_to_path)
import os
import csv
import json
from tqdm import tqdm 
def extract_image_url(jsonl_path, url_list_file):  
    print("Counting lines in jsonl file...")
    total = 0
    with open(jsonl_path, 'r') as jsonl_file:  
        for line in jsonl_file:  
            total += 1
    print(f"Found {total} lines.")
    print("Extracting image url to {}...".format(url_list_file))
    # make directory if not exist
    if not os.path.exists(os.path.dirname(url_list_file)):
        os.makedirs(os.path.dirname(url_list_file))
    with open(jsonl_path, 'r') as jsonl_file , open(url_list_file, 'w') as url_list:          
        csv_writer = csv.writer(url_list)
        csv_writer.writerow(['url', 'image_id'])
        for line in tqdm(jsonl_file, total=total):
            json_obj = json.loads(line)  
            url = json_obj['url']
            image_id = json_obj['key']
            csv_writer.writerow([url, image_id])

import argparse
if __name__ == '__main__':  
    # you need to download the jsonl before run this file    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsonl_path', type=str, default='./download/grit_coyo.jsonl')
    parser.add_argument('--url_list_file', type=str, default='./download/url_list.csv')
    args = parser.parse_args()
    extract_image_url(args.jsonl_path, args.url_list_file)
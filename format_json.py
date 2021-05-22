import json
import sys
import os

'''
Note that this file does not change the result when downloading data
using the .json file. This is just to label the json dict in order just
in case your value in key-value pair from the json file is wrong

To run
python3 ./format_json.py ./object_html_json/<object>_html.json
'''

def format_json_dict(json_file):
    urls_list = []

    with open(json_file) as f:
        urls = json.load(f)

    count = 1
    for url, i in urls.items():
        urls[url] = count
        count += 1

    with open (json_file, 'w') as outfile:
        json.dump(urls, outfile, indent=4)
    return urls_list


def main():
    file_path = sys.argv[-1]
    format_json_dict(file_path)


if __name__ == '__main__':
    main()
# Object Properties Information Extraction
This repository contains information and tool that is used to download web content information from **Amazon** only.

The original usage of this repository is for my final year project - Exploratory action selection for discovering object properties - which is mainly a deep learning project that aims to use NLP method to extract information from text.

Since this is a novel problem, data collection is needed and this repo has the following purpose and usage:
- Download product information (text) from **Amazon** only and generate the information into a spreadsheet (.xslx) for data labelling
- Download the corresponding product image

### Usage and workflow of the main script `./script.py`
1. Create `./object_html_json/<object_name>_html.json` file which contains an array of the object links
2. Run the script by `python3 ./script.py` which will generate the 

### Sample output from console


### Repository Structure
- `./script.py`: a script that is used to download product information from Amazon
- `./images/` contains the images of different objects, corresponding to the links in `./object_html_json/<object>.json`


## Current status of the number of available product information

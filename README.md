# Object Properties Information Extraction
This repository contains information and tool that is used to download web content information from **Amazon** only.

The original usage of this repository is for my final year project - Exploratory action selection for discovering object properties - which is mainly a deep learning project that aims to use NLP method to extract information from text.

Since this is a novel problem, data collection is needed and this repo has the following purpose and usage:
- Download product information (text) from **Amazon** only and generate the information into a spreadsheet (.xslx) for data labelling
- Download the corresponding product image

### Sections that are downloaded from Amazon (in order)
- Product title
- 'Product Table' (Above **About this item**)
- About this item
- Technical Details

### Usage and workflow of the main script `./script.py`
1. Create `./object_html_json/<object_name>_html.json` file which contains an array of the object links
2. Run the script by `python3 ./script.py -f <tartget-json-file> -obj <object-name>` which will generate a spreadsheet in `.xlsx` format for labelling
3. To download image (if you need to), I recommend you do this after you generated the spreadsheet in a separate sesson as this can reduce the work load if you were doing this in one go. The image can be downloaded by using `python3 ./script.py -f <tartget-json-file> -obj <object-name> -img true`

Examples:

To generate the `web_scrape_mug.xlsx`

`python3 ./script.py -f ./object_html_json/mug_html.json -obj mug`

To download images for **mug**

`python3 ./script.py -f ./object_html_json/mug_html.json -obj mug -img true`
### Data collection from Amazon (Manually adding link to your .json file)
There are things that need to be aware of when you are collecting the links required for the `.json` file before generating the spreadsheet, which will be descible below.

Work flow
- Go to https://www.amazon.co.uk/ and search your require object/product (e.g. a mug)
- When you are selecting which product you want to add to your dataset, avoid adding the product which has the **Sponsored** label or within the **Recommended article** section. This is because these advertised product are likely to re-appear again in the next pages, we try to avoid it to prevent duplicate data. (Shown in the image below)
- Secondly try to avoid selecting a product which is a set (e.g. set of mugs, 4 baking tray, 3 plates, etc.)
![image info](./readme_src/amazon_web_scrape_example.png)

### Changes to the code
Note that sometime the program does not run if you access it too often (As you may see from my comment in `./script.py` that Amazon will block bot access). Therefore if you see there are all exceptions in the console output please change the `sess.headers['User-Agent']` defined in the main
### Repository Structure
- `./script.py`: a script that is used to download product information from Amazon
- `./images/` contains the images of different objects, corresponding to the links in `./object_html_json/<object>.json`


## Current status of the number of available product information
| Object      | Spreadsheet             | Image               | Labelled?           |
| :---        |    :----:               |        :----:       |                ---: |
| Mug         | :white_check_mark:      | :white_check_mark:  | :white_check_mark:  |
| Kettle      | :white_check_mark:      | :white_check_mark:  | :white_check_mark:  |
| Bottle      | :white_check_mark:      | :white_check_mark:  | :white_check_mark:  |
| Baking tray | :white_check_mark:      | :white_check_mark:  | |

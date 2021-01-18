import json
with open('./object_html.json') as f:
    data = json.load(f)

for url in data:
    print(url)
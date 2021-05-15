import requests
import pprint
import json
import time
from bs4 import BeautifulSoup


urls_list = []
with open('./object_html_json/bottle_html.json') as f:
    urls = json.load(f)

for url in urls:
    urls_list.append(url)


sess = requests.Session()
# sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

def get_product_image(sess, url, img_number):
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    image_url = soup.find(id='imgTagWrapperId')
    link = image_url.find_all('img')
    f = open('./Images/mug/mug' + str(img_number) + '.jpg', 'wb')
    f.write(requests.get(link[0]['data-old-hires']).content)
    f.close()
    # print(link[0]['src'])
###########################################################################
# Download images
# Now download the image to the ./Images/<object>/folder
# get_product_image(sess, urls_list[10], 11)
# for i in range(len(urls_list)):
#     try:
#         get_product_image(sess, urls_list[i], i+1)
#     except:
#         print("Mug " + str(i+1) + " has exception, cannot be downloaded automatically")
###########################################################################

def get_product_info(sess, url):
    # URL = ('https://www.amazon.co.uk/Opard-Coffee-Insulation-Stainless-Leakproof/dp/B086DKTVQ1/ref=sr_1_21?dchild=1&keywords=mug&qid=1608929241&sr=8-21&th=1')
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    output = ''

    product_title = soup.find(id='productTitle').text.strip()
    # print('Product title is :{}'.format(product_title.strip()))
    # print('\n=====Printing product title=====\n')
    # print(product_title)
    output = output + product_title + '\n'


    product_table = soup.find("table", attrs={"class": "a-normal a-spacing-micro"})
    if product_table is not None:
        product_table_data = product_table.find_all("tr")

        # print("\n=====Printing the table above \'About this item\'=====\n")
        # print(product_table_data)

        table_data = []
        for entry in product_table_data:
            tds = entry.find_all("td")
            table_data = []
            for td in tds:
                table_data.append(td.text.strip())
            output = output + ' '.join(table_data) + '\n'

    # print('\n=====Now printing about this item=====\n')

    about_this_item = soup.find("ul", attrs={"class": "a-unordered-list a-vertical a-spacing-mini"})
    # print(about_this_item)
    if about_this_item is not None:
        for li in about_this_item.find_all('li'):
            output = output + li.text.strip() + '\n'
        # print(li.text.strip())

    # print('\n=====Now printing Technical Details=====\n')

    technical_detail = soup.find("table", attrs={"class": "a-keyvalue prodDetTable"})
    if technical_detail is not None:
        technical_detail_data = technical_detail.find_all("tr")
        if technical_detail_data is not None:
            for entry in technical_detail_data:
                tds = entry.find_all("td")
                ths = entry.find_all("th")
                table_data = []
                table_data_head = []
                for th in ths:
                    table_data_head.append(th.text.strip())
                for td in tds:
                    table_data.append(td.text.strip())
                result = [list(zipped) for zipped in zip(table_data_head, table_data)]
                for res in result:
                    output = output + ' '.join(res) + '\n'

    # print('***Finished createing the string***')
    return output



###########################################################################
#  Now writing to xlsx file
# import xlsxwriter

# output1 = get_product_info(sess, urls_list[0])
# # print(output1)
# # print(len(urls_list))
# workbook = xlsxwriter.Workbook('./SpreadSheet/web_scrape_bottle.xlsx')
# worksheet = workbook.add_worksheet()
# for i in range(1, len(urls_list) + 1):
#     try:
#         output = get_product_info(sess, urls_list[i-1])
#         worksheet.write('A' + str(i), output)
#         print('*** Successfully writen to A{} cell'.format(str(i)))
#     except:
#         print('Exception in {}', urls_list[i-1])
# workbook.close()

###########################################################################

# Testing individual link
testUrl = "https://www.amazon.co.uk/Minecraft-Bottle/dp/B07PZCZZ7S/ref=sr_1_136?dchild=1&keywords=bottle&qid=1620470167&sr=8-136"
test_output = get_product_info(sess, testUrl)
print(test_output)
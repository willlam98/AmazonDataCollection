import requests
import pprint
import json
import time
import xlsxwriter
import os
from cli_parser.CLIParser import CLIParser
from bs4 import BeautifulSoup

def get_product_image(sess, url, img_number, object):
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    image_url = soup.find(id='imgTagWrapperId')

    link = image_url.find_all('img')
    if not os.path.exists('./images/{}'.format(object)):
        os.makedirs('./images/{}'.format(object))
    f = open('./images/{}/{}'.format(object, object) + str(img_number) + '.jpg', 'wb')
    try:
        f.write(requests.get(link[0]['data-old-hires']).content)
    except:
        f.write(requests.get(link[0]['src']).content)
    f.close()
    print('Successfully downloaded image from link {}'.format(img_number))


def get_product_info(sess, url):
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    output = ''
    unstructured = ''
    structured = ''

    # Get product title (Unstructured)
    product_title = soup.find(id='productTitle').text.strip()
    output = output + product_title + '\n'
    unstructured = unstructured + product_title + '\n'

    # Get the table above 'Above this item' (Structured)
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
            structured = structured + ' '.join(table_data) + '\n'

    # print('\n=====Now printing about this item=====\n')
    # Unstructured
    about_this_item = soup.find("ul", attrs={"class": "a-unordered-list a-vertical a-spacing-mini"})
    # print(about_this_item)
    if about_this_item is not None:
        for li in about_this_item.find_all('li'):
            output = output + li.text.strip() + '\n'
            unstructured = unstructured + li.text.strip() + '\n'
    # print('\n=====Now printing Technical Details=====\n')
    # Structured
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
                    structured = structured + ' '.join(res) + '\n'

    # print('***Finished createing the string***')
    return output, unstructured, structured

###########################################################################
#  Now writing to xlsx file
def write_spreadsheet(sess, urls_list, obj):
    workbook = xlsxwriter.Workbook('./spreadsheet/web_scrape_{}.xlsx'.format(obj))
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Input')
    worksheet.write('B1', 'UnstructuredText')
    worksheet.write('C1', 'StructuredText')
    for i in range(1, len(urls_list) + 1):
        try:
            output, unstructured, structured = get_product_info(sess, urls_list[i-1])
            worksheet.write('A' + str(i+1), output)
            worksheet.write('B' + str(i+1), unstructured)
            worksheet.write('C' + str(i+1), structured)
            print('*** Successfully writen to A{idx}, B{idx}, C{idx} cell'.format(idx = str(i+1)))
        except:
            print('Exception in {}'.format(urls_list[i-1]))
    workbook.close()

###########################################################################

def get_urls_list(json_file):
    urls_list = []

    with open(json_file) as f:
        urls = json.load(f)

    for url in urls:
        urls_list.append(url)

    return urls_list

def main():
    cli_parser = CLIParser()
    json_file, obj, download_img = cli_parser.parse()

    sess = requests.Session()
    '''
    sess.headers['User-Agent'] needs to be changed sometime as this might get blocked by
    Amazon if high traffic (Apparently Amazon do not want bot to access their website)
    Look at https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/ for more details
    '''
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    sess.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'
    urls_list = get_urls_list(json_file)


    if json_file is not None and obj is not None and download_img is None:
        write_spreadsheet(sess, urls_list, obj)
    if download_img is not None and download_img == 'true':
        err_log = []
        for i in range(len(urls_list)):
            try:
                get_product_image(sess, urls_list[i], i+1, obj)
            except:
                msg = '{} {} has exception, cannot be downloaded automatically\n'.format(obj, str(i+1))
                print(msg)
                err_log.append(msg)
        log_file = open('./download_image.log', 'w')
        for err in err_log:
            log_file.write(err)

    ## Testing individual link ---> need to uncomment the above
    # If you want to test individual link, run without options
    # python3 ./script.py
    # testUrl = 'https://www.amazon.com.au/Bodum-Chambord-French-Coffee-Ounce-5/dp/B00012D0R2/ref=sr_1_2?dchild=1&keywords=coffee+maker&qid=1621968636&sr=8-2'
    # output, unstructured, structured = get_product_info(sess, testUrl)
    # print('output:\n{}\n\nunstructured:\n{}\n\nstructured:\n{}'.format(output, unstructured, structured))

if __name__ == '__main__':
    main()

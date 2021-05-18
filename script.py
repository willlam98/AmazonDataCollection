import requests
import pprint
import json
import time
import xlsxwriter
from cli_parser.CLIParser import CLIParser
from bs4 import BeautifulSoup

def get_product_image(sess, url, img_number, object):
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    image_url = soup.find(id='imgTagWrapperId')
    link = image_url.find_all('img')
    f = open('./images/{}/{}'.format(object, object) + str(img_number) + '.jpg', 'wb')
    f.write(requests.get(link[0]['data-old-hires']).content)
    f.close()
    print('Successfully download image from {}'.format(img_number))


def get_product_info(sess, url):
    res = sess.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    output = ''
    print(soup)
    product_title = soup.find(id='productTitle').text.strip()
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
def write_spreadsheet(sess, urls_list, obj):
    workbook = xlsxwriter.Workbook('./spreadsheet/web_scrape_.xlsx'.format(obj))
    worksheet = workbook.add_worksheet()
    for i in range(1, len(urls_list) + 1):
        try:
            output = get_product_info(sess, urls_list[i-1])
            worksheet.write('A' + str(i), output)
            print('*** Successfully writen to A{} cell'.format(str(i)))
        except:
            print('Exception in {}', urls_list[i-1])
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
    json_file, obj, download_img= cli_parser.parse()

    sess = requests.Session()
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    # sess.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    sess.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    urls_list = get_urls_list(json_file)

    if json_file is not None and obj is not None and download_img is None:
        write_spreadsheet(sess, urls_list, obj)
    if download_img is not None and download_img == 'True':
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

    ## Testing individual link
    # testUrl = "https://www.amazon.co.uk/Funny-mug-Humour-Christmas-Present/dp/B01M64Y51R/ref=sxin_9_ac_d_rm?ac_md=1-1-ZnVubnkgbXVn-ac_d_rm&cv_ct_cx=mug&dchild=1&keywords=mug&pd_rd_i=B01M64Y51R&pd_rd_r=6b991db5-8485-4e66-97c8-5d3192c5968f&pd_rd_w=orMxD&pd_rd_wg=6mERK&pf_rd_p=0c799c14-fd2d-4652-a647-3581649b0ff7&pf_rd_r=GZYCD9W91BQ6SNFC5774&psc=1&qid=1608929241&sr=1-2-fe323411-17bb-433b-b2f8-c44f2e1370d4"
    # test_output = get_product_info(sess, testUrl)
    # print(test_output)

if __name__ == '__main__':
    main()

import os
import urllib 
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import json
import xlwt

from .models import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 销量  st=8
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=8&iy=0&n=1&sesab=&id=IDENTIFYING&cc=731&jzq=174106
# 综合 st=0
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=0&iy=0&n=1&sesab=&id=IDENTIFYING&cc=731&jzq=19198
# 评价数  st=6
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=6&iy=0&n=1&sesab=&id=IDENTIFYING&cc=731&jzq=1130689
# 价格  st=9 升序
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=9&iy=0&n=1&sesab=&id=IDENTIFYING&cc=731&jzq=19198
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=9&iy=0&n=1&sesab=ACAABAAB&id=IDENTIFYING&cc=731&jzq=136683
# https://search.suning.com/emall/searchV1Product.do?keyword=%E7%94%B5%E8%84%91&ci=0&pg=01&cp=0&il=0&st=9&iy=0&n=1&sesab=ACAABAAB&id=IDENTIFYING&cc=731&jzq=142951
# 价格  st=10  降序
# https://search.suning.com/emall/searchV1Product.do?keyword=%E6%89%8B%E6%9C%BA&ci=0&pg=01&cp=0&il=0&st=10&iy=0&n=1&sesab=ACAABAAB&id=IDENTIFYING&cc=731&jzq=18732

SORT_KEY = {
    '1':'0',
    '2':'8',
    '3':'6',
    '4':'9',
    '5':'10'
}

SORT_DATA = {
    '1':'综合',
    '2':'销量',
    '3':'人气',
    '4':'价格升序',
    '5':'价格降序'
}

def get_html(url, search_data, sort_num, uword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}


    start_url = 'https://search.suning.com/{}/#second-filter'.format(uword)
    newurl = url + '?' + uword + '&ci=0&pg=01&cp=0&il=0&iy=0&n=1&sesab=ACAABAAB&id=IDENTIFYING'


    sort_url = newurl + '&st={}'.format(SORT_KEY[sort_num])

    # response = requests.get(start_url, headers=headers)
    response = requests.get(sort_url, headers=headers, verify=False)
    response.encoding = 'utf-8'  
    get_info(response, search_data, sort_num, uword)

def get_info(response, search_data, sort_num, uword):
    try:
        content = etree.HTML(response.text)
        # print(response.text)
        print('苏宁　content', content)
       
        for i in range(10):
            # title = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-info"]/div[@class="title-selling-point"]/a/text')[i]
            # title = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-info"]/div[@class="title-selling-point"]/a/@title')[i]

            tit = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-info"]/div[@class="title-selling-point"]')[i]
            title = tit.xpath('string(.)').strip()

            shop = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-info"]/div[@class="store-stock"]/a/text()')[i]
            comment = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-info"]/div[@class="evaluate-old clearfix"]/div[@class="info-evaluate"]/a/i/text()')[i] + '评价'
            img = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-img"]/div[@class="img-block"]/a/img/@src')[i]
            link = content.xpath('//div[@class="item-bg"]/div[@class="product-box"]/div[@class="res-img"]/div[@class="img-block"]/a/@href')[i]
            
            ids = content.xpath('//li/@id')[i] 
            pid = ids.split('-')[0]
            skuid = ids.split('-')[1]

            price = get_price(pid, skuid)

            # print(search_data, SORT_DATA[sort_num], pid, skuid, price, title.strip(), shop, comment, img, link)
            Sn.objects.create(search=search_data, sort=SORT_DATA[sort_num], title=title, price=price, shop=shop, img=img, link=link)
    
    except Exception as e:
        print('e----->', e)
    

# https://ds.suning.cn/ds/generalForTile/000000000690105206,-731-2-0000000000-1--ds000000000916.jsonp?
# https://ds.suning.cn/ds/generalForTile/774034025__2_0070073500,-731-2-0000000000-1--ds000000000916.jsonp?
def get_price(pid, skuid):

    url1 = 'https://ds.suning.cn/ds/generalForTile/{},-731-2-0000000000-1--ds000000000916.jsonp?'.format(skuid)
    url2 = 'https://ds.suning.cn/ds/generalForTile/{}__2_{},-731-2-0000000000-1--ds000000000916.jsonp?'.format(skuid, pid)

    try:
        if pid == '0000000000':
            response = requests.get(url1, verify=False)
            response.encoding = 'utf-8'
        else:
            response = requests.get(url2, verify=False)
            response.encoding = 'utf-8'
    except Exception as e:
        print('e----------------------->', e)
    # print(response.text)

    if response.content:
        data = json.loads(response.text.lstrip('ds000000000916(').rstrip(');'))
        rs = data['rs']
        for s in rs:
            price = s['price']
            # print('price-------------------------------', price)
            return price
    return None    


def sn_main(search_data, sort_num, uword):
    url = 'https://search.suning.com/emall/searchV1Product.do'
    get_html(url, search_data, sort_num, uword)

if __name__ == '__main__':
    sn_main(search_data, sort_num, uword)


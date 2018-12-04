
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=844cfc1a13844dfaa84da14c4ad425ca
# 评论数  psort=4
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&psort=4&cid2=653&cid3=655&click=0

# 综合
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&click=0
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8
# 销量   psort=3
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&psort=3&cid2=653&cid3=655&click=0

# 新品   psort=5
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&psort=5&cid2=653&cid3=655&click=0

# 价格   psort=2
# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&psort=2&cid2=653&cid3=655&click=0


import os
import urllib 
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import sys
import re
import csv
from .models import *

# sys.setdefaultencoding('unicode')

SORT_KEY = {
    '1':'0',
    '2':'3',
    '3':'4',
    '4':'1',  
    '5':'2'
}
SORT_DATA = {
    '1':'综合',
    '2':'销量',
    '3':'人气',
    '4':'价格升序',
    '5':'价格降序'
}
cookie_str = r'__jdu=1189001422; PCSYCityID=country_2468; shshshfpa=1a029c8b-f4f8-416d-c891-8afac70f3c3c-1541941414; shshshfpb=0c7b40e51031f798950ed32d0847440cfbd474252ceabf87f5be828a97; ipLoc-djd=1-72-4137-0; areaId=1; mt_xid=V2_52007VwMSW1VZU1oaShpsA28AEgVUWFFGG0AdWxliURpXQQtXUhdVHQgNb1RFVFxbVggfeRpdBW4fElJBWFJLHEkSXQBsBxJiX2hSahZJG14EbgcbW11QVl8dSxFYB2YzF1s%3D; unpl=V2_ZzNtbUpeRUVxDhJRfB1YV2JRE1oRUhAXdF9PAX8QWw1kUUcOclRCFXwURlRnGV4UZAMZWUpcRhVFCHZUehhdBGYBFV5GZxpFKwhFVidSbDVkAyJVcldDHH0JR1R%2bGl81VwQibXJWcxRFCXYfFRgRBWcKGlxDV0YWdjhHZHg%3d; __jdc=122270672; __jdv=122270672|www.hao123.com|t_1000003625_hao123mz|tuiguang|987a57e4655c4c06b4b30f8d58692cdb|1542117584489; shshshfp=79f1515d21d05270fd555d6d7099e042; __jda=122270672.1189001422.1541941405.1542117584.1542123799.3; shshshsID=0c0f0dfee67ea8a9529bf0b17d24d9f9_10_1542123927971; wlfstk_smdl=p1wfnam61lrnetb77nyd88m1k1xat71j; thor=56375DA852D9E4143AC13B0DA436EA6259CDC0023635109BC3266373F9F9EFE485A7AE470CFD2313EA9F077CABDA5AA831002170D22A29C011825F5CF3D7F3487327847F62F410A8C7C8B30A0A365C1EFD6962334F8C12C01F91608A259528415904A762B5A0F672D3B07908CF6C53B5F465DC4108A88B8EBA12A99F811CFD33051FEFB434D15E5F1F13D6572047F673EB4085C3D9FEC920144B3AAF6D8CC1C9; unick=jd_7bdf62193d690; 3AB9D23F7A4B3C9B=K4Q4VSADTEPPJBYWSPYOJ2VKQMLFBYOPTJM4WREUOSJIVB34M4YA5IQZYQZ6MO5O6S7IAQYCRBAM4LJ4P6T7RUSPBY; __jdb=122270672.27.1189001422|3.1542123799'

cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value

def get_html(url, search_data, sort_num, uword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

    newurl = url + '?' + uword + '&enc=utf-8' 
    
    sort_url = newurl + 'psort=%s'%SORT_KEY[sort_num]

    response = requests.get(sort_url, headers=headers, cookies=cookies)
    response.encoding = 'utf-8'     #########

    get_info(response, search_data, sort_num)

def get_info(response, search_data, sort_num):
    try:
        content = etree.HTML(response.text)
        # print(response.text)
        print('京东　content', content)
        
        for i in range(10):
            try:
      
                # try:
                #     x1 = '//*[@id="J_goodsList"]/ul/li[%d]/div/div[4]/a/em'%(i+1)
                # except Exception as e:
                #     print('e--->', e)
                    # x1 = '//*[@id="J_goodsList"]/ul/li[%d]/div/div[4]/a/em/img'%(i+1)
                # # else:
                #     x1 = '//*[@id="J_goodsList"]/ul/li[%d]/div/div[4]/a/em/span'%(i+1)
                # title = content.xpath(x1)[0].text

                t1 = content.xpath('//*[@id="J_goodsList"]/ul/li[%d]/div/div[4]/a/em'%(i+1))
                title = t1[0].xpath('string(.)').strip()

                # title = content.xpath('////*[@id="J_goodsList"]/ul/li[%d]/div/div[4]/a/@title'%(i+1))[0]
                            
                price = content.xpath('//ul[@class="gl-warp clearfix"]//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()')[i]
                
            
                try:
                    shop = content.xpath('//ul[@class="gl-warp clearfix"]//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-shop"]/span/a/text()')[i]
                except Exception as e:
                    shop = '自营'
                try:
                    img = content.xpath('//ul[@class="gl-warp clearfix"]//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-img"]/a/img')[i].attrib['source-data-lazy-img']
                except Exception as e:
                    img = 'img'

                try:
                    link = content.xpath('//ul[@class="gl-warp clearfix"]//li[@class="gl-item"]/div[@class="gl-i-wrap"]/div[@class="p-img"]/a/@href')[i]
                except Exception as e:
                    link = 'img'

                # print(title, price, shop, img, link)


                Jd.objects.create(search=search_data, sort=SORT_DATA[sort_num], title=title, price=price, shop=shop, img=img, link=link)

            except Exception as e:
                print('e------->', e)
                return
 

    except Exception as e:
        print('e--------------->', e)
        return


def jd_main(search_data, sort_num, uword):
    url = 'https://search.jd.com/Search'
    get_html(url, search_data, sort_num, uword)

if __name__ == '__main__':
    jd_main(search_data, sort_num, uword)
    
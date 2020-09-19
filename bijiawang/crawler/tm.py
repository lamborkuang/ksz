import os
import urllib 
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
from redis import *
from .models import *
import time 

SORT_KEY = {
    '1':'s',
    '2':'d',
    '3':'rq',
    '4':'p',
    '5':'pd'
}

SORT_DATA = {
    '1':'综合',
    '2':'销量',
    '3':'人气',
    '4':'价格升序',
    '5':'价格降序'
}


cookie_str = r't=919139c17300c32ce6dc7ef5ae20d31c; cna=GQlvFIzEbHACAXcn+DELJWGy; tracknick=%5Cu6DD1%5Cu5E862012; lgc=%5Cu6DD1%5Cu5E862012; tg=0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; mt=ci=-1_1&np=; _m_h5_tk=222867d1a1829ce0718bb4777b3a6dbf_1542038511272; _m_h5_tk_enc=af930d3e6d35b2f6c37dbd6969e35f3d; enc=BGtkUW6mQxftcoO%2FnEl%2B63LuzYOvPTd1jj9601qQOC9oXgEv9hKEpYmSeF3Q%2BXTJCQcwsAIoySoUxvxjTzSpBg%3D%3D; cookie2=10ef0fbe3c28f5c57b7a29c70710d35c; _tb_token_=e34553e7e56bd; v=0; _mw_us_time_=1542118595606; unb=1072402482; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=Vq8l%2BKCLjhZM&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=false&pas=0&cookie14=UoTYNO6HA0UxPQ%3D%3D&tag=8&lng=zh_CN; sg=22b; _l_g_=Ug%3D%3D; skt=8b0c7cc7dbeba305; cookie1=Vy7u1h3e1wkyGYsGfLX%2BWWLeXTaq6Z93jegXiyHdbOs%3D; csg=7f655616; uc3=vt3=F8dByR%2FNWx6YOj4SuDo%3D&id2=UoH4F%2BEW%2BFTNpg%3D%3D&nk2=qXX%2Fzrcruw0%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; existShop=MTU0MjExODYwMw%3D%3D; _cc_=WqG3DMC9EA%3D%3D; dnk=%5Cu6DD1%5Cu5E862012; _nk_=%5Cu6DD1%5Cu5E862012; cookie17=UoH4F%2BEW%2BFTNpg%3D%3D; isg=BGRk0Wav4z0mzhfzNWNY0yYoNWKWVYADoKv2436F8C_yKQTzpg1Y95qP7ceU8cC_'

cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value


def get_html(url, search_data, sort_num, uword):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

    word1 = {"q":search_data, 'sort':SORT_KEY[sort_num]}
    uword_sort = urllib.parse.urlencode(word1)

    sort_url = url + '?' + uword_sort    

    response = requests.get(sort_url, headers=headers, cookies=cookies)
    synthesize(response, search_data, sort_num, uword)


def synthesize(response, search_data, sort_num, uword):
    try:
        content = etree.HTML(response.text)
        # print(response.text)
        print('天猫　content', content)

        for i in range(10):
            try:
                price = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]/div[@class="product-iWrap"]/p[@class="productPrice"]/em/text()')[i]
            except Exception as e:
                price = '待定'

            try:
                try:
                    # title = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productTitle productTitle-spu"]/a/@title')[i]
                    tit = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productTitle productTitle-spu"]')[i]
                    title = tit.xpath('string(.)').strip()
                except:
                    # title = content.xpath('//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productTitle"]/a/@title')[i]
                    tit = content.xpath('//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productTitle"]')[i]
                    title = tit.xpath('string(.)').strip()
            except Exception as e:
                title = None

            try:
                shop = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productShop"]/a[@class="productShop-name"]/text()')[i]
            except Exception as e:
                shop = None
                
            '''
                以下这段为什么只能爬取５个图片，其他的都是list index out of range
            '''
            # try:
            #     img = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productImg-wrap"]/a/img/@src')[i]
                
            # except IndexError as f:
            #     img = ""

            # except Exception as e:
               
            #     img = content.xpath('//div[@class="view  view-noCom"]//div[@class="product album-sub "]//div[@class="product-iWrap"]/div[@class="productAlbum"]/a/img/@src')[i]

            try:
                img = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productImg-wrap"]/a/img/@src')[i]
            except Exception as e:
                status = ''

            try:
                link = content.xpath('//div[@class="view  view-noCom"]//div[@class="product  "]//div[@class="product-iWrap"]/div[@class="productImg-wrap"]/a/@href')[i]
            except Exception as e:
                link = '' 

            # print(search_data, SORT_DATA[sort_num], title, price, shop, img, link)

            Tm.objects.create(search=search_data, sort=SORT_DATA[sort_num], title=title, price=price, shop=shop, img=img, link=link)
            
        
    except Exception as e:
        print('e----->', e)
        return

def tm_main(search_data, sort_num, uword):

    url = 'https://list.tmall.com/search_product.htm'
    get_html(url, search_data, sort_num, uword)

if __name__ == '__main__':

    word = {"q":'手机'}
    uword = urllib.parse.urlencode(word)    
    tm_main(search_data, sort_num, uword)
    



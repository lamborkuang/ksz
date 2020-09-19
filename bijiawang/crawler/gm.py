
import os
import urllib 
import requests
from lxml import etree
import json
from .models import *

from w3lib.html import remove_tags

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 价格  sort=21
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&sort=21
# 评价  sort=50
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&sort=50
# 新品   sort=30
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&sort=30
# 销量    sort=10
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&sort=10
# 综合   sort=00
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&sort=00&pzin=v4

# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&deliv=0&sort=50&instock=1&market=10&pzpq=0&pzin=v4&page=1&bws=0&type=json

SORT_KEY = {
    '1':'00',
    '2':'10',
    '3':'50',
    '4':'21',
    '5':'20'
}

SORT_DATA = {
    '1':'综合',
    '2':'销量',
    '3':'人气',
    '4':'价格升序',
    '5':'价格降序'
}


cookie_str = r"uid=CjozJlvpfgZQf276E5ZIAg==; __clickidc=88308210342029149; __c_visitor=88308210342029149; __gmv=1065008770932.1542029149525; cartnum=0_0-1_0; _smt_uid=5be97f61.58e2ee32; compare=; isnew=251067553375.1542205369752; asid=eba7d5942b2a179520808e6880d49124; __gma=ffb8de7.1065008770932.1542029149525.1542207490449.1542293342332.4; __gmc=ffb8de7; atgregion=42010100%7C%E6%B9%96%E5%8D%97%E7%9C%81%E9%95%BF%E6%B2%99%E5%B8%82%E8%8A%99%E8%93%89%E5%8C%BA%E6%9C%9D%E9%98%B3%E8%A1%97%E8%A1%97%E9%81%93%7C42010000%7C42000000%7C420101001; s_cc=true; gpv_p22=no%20value; s_sq=%5B%5BB%5D%5D; DSESSIONID=756b45435f2d45d79f50610b82f2295d; _idusin=77934357888; s_ev13=%5B%5B'dh_360_yx_mz'%2C'1542029235085'%5D%2C%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1542293482259'%5D%5D; route=a4740778113c5452684f57d9d18e1433; gradeId=-1; _index_ad=1; __gmz=ffb8de7|sem_baidu_pinpai_yx_pc_bt|-|sem|-|1gwVvwkg2oEE|-|1065008770932.1542029149525|dc-1|1542293342332; __gmb=ffb8de7.3.1065008770932|4.1542293342332; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216708198628177-03f8a40877c7b9-594c2a16-2073600-16708198629683%22%2C%22%24device_id%22%3A%2216708198628177-03f8a40877c7b9-594c2a16-2073600-16708198629683%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22_latest_cmpid%22%3A%22sem_baidu_pinpai_yx_pc_bt%22%7D%7D; __xsptplus194=194.4.1542293348.1542293514.3%232%7Csp0.baidu.com%7C%7C%7C%25E5%259B%25BD%25E7%25BE%258E%7C%23%23pRME3EH-MLeko4FWId34xd2h8Pf1ODj8%23; gpv_pn=no%20value; s_getNewRepeat=1542293537144-Repeat; s_ppv=-%2C31%2C16%2C2210; plasttime=1542294478"
cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value
# 此headers 只用于get_data用，其他的可能会报错   注意下面的question=%E6%89%8B%E6%9C%BA可能需要更改
headers = '''

            Host: search.gome.com.cn
            Connection: keep-alive
            Accept: application/json, text/javascript, */*; q=0.01
            X-Requested-With: XMLHttpRequest
            User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36
            Referer: https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&searchType=goods&search_mode=normal
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9
            Cookie: __clickidc=88308210342029149; __c_visitor=88308210342029149; __gmv=1065008770932.1542029149525; _smt_uid=5be97f61.58e2ee32; compare=; asid=eba7d5942b2a179520808e6880d49124; uid=CjozJlv0GFJz50WuR7XjAg==; cartnum=0_0-1_0; isnew=711973787884.1542894721979; __gmc=ffb8de7; atgregion=42010100%7C%E6%B9%96%E5%8D%97%E7%9C%81%E9%95%BF%E6%B2%99%E5%B8%82%E8%8A%99%E8%93%89%E5%8C%BA%E6%9C%9D%E9%98%B3%E8%A1%97%E8%A1%97%E9%81%93%7C42010000%7C42000000%7C420101001; s_cc=true; _idusin=78026857179; route=f77df931395593f2f42edc4edcbeb9a0; gradeId=-1; s_ev13=%5B%5B'dh_360_yx_mz'%2C'1542029235085'%5D%2C%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1542894639915'%5D%2C%5B'sem_baidu_cpc_yx_pc1_%25u54C1%25u724C%25u8BCD-%25u56FD%25u7F8E-%25u5168%25u56FD_%25u56FD%25u7F8E-%25u6838%25u5FC3_%25u56FD%25u7F8E'%2C'1542894640168'%5D%2C%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1542894707537'%5D%2C%5B'sem_baidu_cpc_yx_pc1_%25u54C1%25u724C%25u8BCD-%25u56FD%25u7F8E-%25u5168%25u56FD_%25u56FD%25u7F8E-%25u6838%25u5FC3_%25u56FD%25u7F8E'%2C'1542894714809'%5D%2C%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1543066713182'%5D%5D; DSESSIONID=3dbe73385d2c40f989079a79c355b089; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216708198628177-03f8a40877c7b9-594c2a16-2073600-16708198629683%22%2C%22%24device_id%22%3A%2216708198628177-03f8a40877c7b9-594c2a16-2073600-16708198629683%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22_latest_cmpid%22%3A%22sem_baidu_pinpai_yx_pc_bt%22%7D%7D; __xsptplus194=194.12.1543068717.1543069538.5%233%7Cbzclk.baidu.com%7C%7C%7C%7C%23%23i1NMS3BhcpLedT4qvP_jDTmokDBCczO8%23; s_ppv=-%2C94%2C22%2C6694; __gma=ffb8de7.1065008770932.1542029149525.1543068706498.1543075189083.13; __gmb=ffb8de7.1.1065008770932|13.1543075189083; __gmz=ffb8de7|www.gome.com.cn|-|referrer|-|1gLOMoTIdMsE|-|1065008770932.1542029149525|dc-1|1543075189084; gpv_pn=no%20value; gpv_p22=no%20value; s_getNewRepeat=1543075189096-Repeat; s_sq=gome-prd%3D%2526pid%253Dhttps%25253A%25252F%25252Fsearch.gome.com.cn%25252Fsearch%25253Fquestion%25253D%252525E6%25252589%2525258B%252525E6%2525259C%252525BA%252526searchType%25253Dgoods%252526search_mode%25253Dnormal%2526oid%253Dhttps%25253A%25252F%25252Fsearch.gome.com.cn%25252Fsearch%25253Fquestion%25253D%25252525E6%2525252589%252525258B%25252525E6%252525259C%25252525BA%252526deliv%25253D0%252526sort%25253D00%252526market%25253D10%252526%2526ot%253DA; plasttime=1543075195

    '''


def str2obj(s,s1=';',s2='='):
    li=s.split(s1)
    res={}
    for kv in li:
        kv = kv.strip()
        li2=kv.split(s2)
        if len(li2)>1:

            res[li2[0]]=li2[1]
    return res
headers=str2obj(headers, '\n', ': ')


def get_html(url, search_data, sort_num, uword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

    newurl = url + '?' + uword 

    sort_url = newurl + '&sort={}'.format(sort_num)

    response = requests.get(sort_url, headers=headers, cookies=cookies, verify=False)
    response.encoding = 'utf-8'  

    get_data(sort_url, search_data, sort_num, uword)


# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&deliv=0&sort=30&market=10&pzpq=0&pzin=v4&page=1&bws=0&type=json
def get_data(sort_url, search_data, sort_num, uword):

    newurl = sort_url + '&deliv=0&market=10&pzpq=0&pzin=v4&page=1&bws=0&type=json'
    response = requests.get(newurl, headers=headers, cookies=cookies, verify=False)
    response.encoding = 'utf-8'

    data = json.loads(response.text)
    # print(json.dumps(data,indent=2,ensure_ascii=False))
    skus = data['content']['prodInfo']['products'][:10]
    
    for sku in skus:

        skuid = sku['skuId']
        pid = sku['pId']

        title = sku['name'].replace('<[\s\S].*>', '')
        # remove_tags(title)
        

        try:
            shop = sku['sName']
        except Exception as e:
            shop = '自营'
        img = sku['sImg']
        
        link = sku['sUrl']
        price = get_price(skuid, pid)

        Gm.objects.create(search=search_data, sort=SORT_DATA[sort_num], title=title, price=price, shop=shop, img=img, link=link)
 
        # print(search_data, SORT_DATA[sort_num], skuid, pid, title, shop, img, price, link)
 
# https://ss.gome.com.cn/searcfn1543064129757?callback=fn1543064129757&_=1543064129757h/v1/price/single/9140132337/1130629279/42010000/flag/item/
# https://ss.gome.com.cn/search/v1/price/single/9140132337/1130629279/42010000/flag/item/
def get_price(skuid, pid):
    
    url = 'https://ss.gome.com.cn/search/v1/price/single/{}/{}/42010000/flag/item'.format(pid, skuid)
    # print('get price url------------------------>', url)
    try:
        response = requests.get(url, verify=False)
        response.encoding = 'utf-8'
    except Exception as e:
        print('e----------------------->', e)

    # print(response)
    if response.content:
        
        data = json.loads(response.text)
        price = data['result']['price']
        # print(price)
        return price
    return None
       
def gm_main(search_data, sort_num, uword):
    url = 'https://search.gome.com.cn/search'
    get_html(url, search_data, sort_num, uword)

if __name__ == '__main__':
    gm_main(search_data, sort_num, uword)



# json
# https://flight.gome.com.cn/flight?callback=dsp_tg&p=10044&catid=cat10000070&searchkey=%E6%89%8B%E6%9C%BA&c=dsp_tg&width_height=210-210&area=42010100&requestType=3&_=1543061899157
# https://flight.gome.com.cn/flight?callback=dsp_tg&p=10044&catid=cat10000070&searchkey=%E6%89%8B%E6%9C%BA&c=dsp_tg&width_height=210-210&area=42010100&requestType=3&_=1543061899157

# jiage                            "productId":"9140132337"    "skuId":"1130629279"      fn1543064129757 
# https://ss.gome.com.cn/search/v1/price/single/9140132337/1130629279/42010000/flag/item/fn1543064129757?callback=fn1543064129757&_=1543064129757
# https://ss.gome.com.cn/search/v1/price/single/9140132337/1130629279/42010000/flag/item/

# 请求获取商品skuid
# https://npop-front.gome.com.cn/promotion/promotionLabels?callback=jQuery17104180435191329199_1543068708733&param=%5B%7B%22sku%22%3A%228012392113%22%2C%22price%22%3A%221268.00%22%7D%2C%7B%22sku%22%3A%228012388452%22%2C%22price%22%3A%221898.00%22%7D%2C%7B%22sku%22%3A%228012388492%22%2C%22price%22%3A%221498.00%22%7D%2C%7B%22sku%22%3A%228012387634%22%2C%22price%22%3A%22286.00%22%7D%5D&_=1543069873380
# https://npop-front.gome.com.cn/promotion/promotionLabels?callback=jQuery17104180435191329199_1543068708734&param=%5B%7B%22sku%22%3A%228012444478%22%2C%22price%22%3A%22996.00%22%7D%2C%7B%22sku%22%3A%228012444273%22%2C%22price%22%3A%221199.00%22%7D%2C%7B%22sku%22%3A%228012442270%22%2C%22price%22%3A%225399.00%22%7D%2C%7B%22sku%22%3A%228012440434%22%2C%22price%22%3A%221988.00%22%7D%5D&_=1543069873669
# https://npop-front.gome.com.cn/promotion/promotionLabels?callback=jQuery17104180435191329199_1543068708729&param=%5B%7B%22sku%22%3A%228012439726%22%2C%22price%22%3A%221749.00%22%7D%2C%7B%22sku%22%3A%228012439847%22%2C%22price%22%3A%224399.00%22%7D%2C%7B%22sku%22%3A%228012439548%22%2C%22price%22%3A%222798.00%22%7D%2C%7B%22sku%22%3A%228012438223%22%2C%22price%22%3A%22286.00%22%7D%2C%7B%22sku%22%3A%228012428628%22%2C%22price%22%3A%222099.00%22%7D%2C%7B%22sku%22%3A%228012428357%22%2C%22price%22%3A%221899.00%22%7D%2C%7B%22sku%22%3A%228012425463%22%2C%22price%22%3A%224699.00%22%7D%2C%7B%22sku%22%3A%228012425234%22%2C%22price%22%3A%224799.00%22%7D%5D&_=1543069766344
# https://npop-front.gome.com.cn/promotion/promotionLabels?callback=jQuery17104180435191329199_1543068708731&param=%5B%7B%22sku%22%3A%228012422433%22%2C%22price%22%3A%22198.00%22%7D%2C%7B%22sku%22%3A%228012422189%22%2C%22price%22%3A%22198.00%22%7D%2C%7B%22sku%22%3A%228012421184%22%2C%22price%22%3A%22899.00%22%7D%2C%7B%22sku%22%3A%228012420323%22%2C%22price%22%3A%22719.00%22%7D%2C%7B%22sku%22%3A%228012418050%22%2C%22price%22%3A%22558.00%22%7D%2C%7B%22sku%22%3A%228012414944%22%2C%22price%22%3A%22248.00%22%7D%2C%7B%22sku%22%3A%228012414813%22%2C%22price%22%3A%22196.00%22%7D%2C%7B%22sku%22%3A%228012410516%22%2C%22price%22%3A%22548.00%22%7D%2C%7B%22sku%22%3A%228012409710%22%2C%22price%22%3A%223038.00%22%7D%2C%7B%22sku%22%3A%228012406278%22%2C%22price%22%3A%221355.00%22%7D%2C%7B%22sku%22%3A%228012404605%22%2C%22price%22%3A%223288.00%22%7D%2C%7B%22sku%22%3A%228012402247%22%2C%22price%22%3A%225618.00%22%7D%5D&_=1543069767267

# 向服务器请求数据
# https://search.gome.com.cn/search?question=%E6%89%8B%E6%9C%BA&deliv=0&sort=30&market=10&pzpq=0&pzin=v4&page=1&bws=0&type=json


# comments = html.text.lstrip("/**/ typeof jQuery1124028906430044366505_1537678009345 === 'function' && jQuery1124028906430044366505_1537678009345(").rstrip(');')

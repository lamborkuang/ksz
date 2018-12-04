from django.shortcuts import render
from django.http import HttpResponse
import urllib 
from .tm import *
from .jd import * 
from .sn import * 
from .gm import * 
from threading import Thread

# Create your views here.
def index_view(request):

    return render(request, 'index.html', locals())


def search_tm(search_data, sort_num):
    word = {"q":search_data}
    uword = urllib.parse.urlencode(word) 

    tm_main(search_data, sort_num, uword)


def search_jd(search_data, sort_num):
    word = {"keyword":search_data}
    uword = urllib.parse.urlencode(word)

    jd_main(search_data, sort_num, uword)
    

def search_sn(search_data, sort_num):
    word = {"keyword":search_data}
    uword = urllib.parse.urlencode(word)

    sn_main(search_data, sort_num, uword)


def search_gm(search_data, sort_num):
    word = {"question":search_data}
    uword = urllib.parse.urlencode(word)

    gm_main(search_data, sort_num, uword)

def search_view(request):

    search_data = request.POST.get('search', None)
    sort_num = request.POST.get('sort', None)

    t1 = Thread(target=search_tm, args=(search_data, sort_num))
    t2 = Thread(target=search_jd, args=(search_data, sort_num))
    t3 = Thread(target=search_sn, args=(search_data, sort_num))
    t4 = Thread(target=search_gm, args=(search_data, sort_num))

    sort_data = ''
    uword_sort = ''
    if search_data and sort_num:
        # search_tm(search_data, sort_num)
        # search_jd(search_data, sort_num)
        # search_sn(search_data, sort_num)
        # search_gm(search_data, sort_num)
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # return HttpResponse('crawl Done!')
        return render(request, 'index.html', {'res':'爬虫爬取天猫，京东，苏宁，国美已完毕！！！'})
        # return render(request, 'index.html', {'res':'crawl done！！！'})
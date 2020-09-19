from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Tm(BaseModel):
    search = models.CharField(max_length=256, verbose_name='搜索内容')
    sort = models.CharField(max_length=16, verbose_name='排序依据')
    title = models.CharField(max_length=1024, verbose_name='名称')
    price = models.CharField(max_length=32, verbose_name='价格')
    shop = models.CharField(max_length=32, verbose_name='商店')
    img = models.CharField(max_length=2048, verbose_name='图片')
    link = models.CharField(max_length=2048, verbose_name='超链接', null=True)

    class Meta:
        db_table = 'tm'
        verbose_name = '天猫'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Jd(BaseModel):
    search = models.CharField(max_length=256, verbose_name='搜索内容')
    sort = models.CharField(max_length=16, verbose_name='排序依据')
    title = models.CharField(max_length=1024, verbose_name='名称')
    price = models.CharField(max_length=32, verbose_name='价格')
    shop = models.CharField(max_length=32, verbose_name='商店')
    img = models.CharField(max_length=2048, verbose_name='图片')
    link = models.CharField(max_length=2048, verbose_name='超链接', null=True)

    class Meta:
        db_table = 'jd'
        verbose_name = '京东'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class Sn(BaseModel):
    search = models.CharField(max_length=256, verbose_name='搜索内容')
    sort = models.CharField(max_length=16, verbose_name='排序依据')
    title = models.CharField(max_length=1024, verbose_name='名称')
    price = models.CharField(max_length=32, verbose_name='价格')
    shop = models.CharField(max_length=32, verbose_name='商店')
    img = models.CharField(max_length=2048, verbose_name='图片')
    link = models.CharField(max_length=2048, verbose_name='超链接', null=True)

    class Meta:
        db_table = 'sn'
        verbose_name = '苏宁'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Gm(BaseModel):
    search = models.CharField(max_length=256, verbose_name='搜索内容')
    sort = models.CharField(max_length=16, verbose_name='排序依据')
    title = models.CharField(max_length=1024, verbose_name='名称')
    price = models.CharField(max_length=32, verbose_name='价格')
    shop = models.CharField(max_length=32, verbose_name='商店')
    img = models.CharField(max_length=2048, verbose_name='图片')
    link = models.CharField(max_length=2048, verbose_name='超链接', null=True)

    class Meta:
        db_table = 'gm'
        verbose_name = '国美'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



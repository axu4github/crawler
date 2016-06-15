# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    id              = scrapy.Field() # 编号
    name            = scrapy.Field() # 名称
    price           = scrapy.Field() # 价格
    seller          = scrapy.Field() # 供应商
    prompt          = scrapy.Field() # 促销信息
    classification  = scrapy.Field() # 分类
    brand           = scrapy.Field() # 品牌

# -*- coding: utf-8 -*-
import scrapy
import time
from jd.items import JdItem
from scrapy.loader import ItemLoader


class jdSpider(scrapy.spiders.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ["http://item.jd.com/987695.html"]
    itemInfo = {
        "id": {"xpath": "//div[@id='product-intro']//div[@id='short-share']//span[2]/text()"},
        "name": {"xpath": "//div[@id='itemInfo']//div[@id='name']/h1/text()"},
        "price": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-price']//strong[@id='jd-price']/text()"},
        "seller": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-service']//div[@class='dd']/text()"},
        "prompts": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']/text()"},
        "classification": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']/strong/a/text()"},
        "brand": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']//span[2]/a[1]/text()"},
    }

    def parse(self, response):
        # seller = response.xpath("")

        p = ItemLoader(item=JdItem(), response=response)
        for key, item in self.itemInfo:
            # p.add_xpath(key, item["xpath"])
            print key, item

        p.load_item()

        print "| 商品编号: %s" % "+".join(p.get_output_value('id'))
        print "| 商品名称: %s" % "+".join(p.get_output_value('name'))
        print "| 商品价格: %s" % "+".join(p.get_output_value('price'))
        print "| 供应商: %s" % "+".join(p.get_output_value('seller'))
        print "| 促销信息: %s" % "+".join(p.get_output_value('prompts'))
        print "| 分类: %s" % "+".join(p.get_output_value('classification'))
        print "| 品牌: %s" % "+".join(p.get_output_value('brand'))



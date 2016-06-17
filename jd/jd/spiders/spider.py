# -*- coding: utf-8 -*-
import scrapy
import time
from jd.items import JdItem
from scrapy.loader import ItemLoader

class jdSpider(scrapy.spiders.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://item.jd.com/987695.html", 
        "http://item.jd.com/1253530085.html",
        "http://item.jd.com/1225287.html",
        "http://item.jd.com/1766183610.html"
    ]

    itemOfSelfEmployed = {
        "id": {"xpath": "//div[@id='product-intro']//div[@id='short-share']//span[2]/text()"},
        "name": {"xpath": "//div[@id='itemInfo']//div[@id='name']/h1/text()"},
        "price": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-price']//strong[@id='jd-price']/text()"},
        "seller": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-service']//div[@class='dd']/text()"},
        # "prompts": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']/text()"},
        "classification": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']/strong/a/text()"},
        "brand": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']//span[2]/a[1]/text()"},
    }

    itemOfOther = {
        "id": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='preview-info']//div[@class='sku']/span/text()"},
        "name": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='itemInfo-wrap']//div[@class='sku-name']/text()"},
        "price": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='itemInfo-wrap']//span[@class='p-price']/span/text()"},
        "seller": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='summary-stock']//div[@class='dd']//div[@class='summary-service']/descendant::text()"},
        # "prompts": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']/text()"},
        "classification": {"xpath": "//div[@class='crumb-wrap']//div[contains(@class, 'item')]/a[contains(@clstag, 'mbNav-1')]/text()"},
        "brand": {"xpath": "//div[@class='crumb-wrap']//div[contains(@class, 'item')]/a[contains(@clstag, 'mbNav-4')]/text()"},
    }

    # 判断商品是不是京东自营
    def isSelfEmployed(self, response):
        return bool(response.xpath("//em[@class='u-jd']"))

    def parse(self, response):
        self.item = self.itemOfSelfEmployed if self.isSelfEmployed(response) else self.itemOfOther

        p = ItemLoader(item=JdItem(), response=response)
        for key in self.item:
            p.add_xpath(key, self.item[key]["xpath"])

        p.load_item()
        print "| ==========="
        print "| 商品编号: %s" % "".join(p.get_output_value('id'))
        print "| 商品名称: %s" % "".join(p.get_output_value('name'))
        print "| 商品价格: %s" % "".join(p.get_output_value('price'))
        print "| 供应商: %s" % "".join(p.get_output_value('seller'))
        # print "| 促销信息: %s" % "+".join(p.get_output_value('prompts'))
        print "| 分类: %s" % "".join(p.get_output_value('classification'))
        print "| 品牌: %s" % "".join(p.get_output_value('brand'))
        print "| ==========="


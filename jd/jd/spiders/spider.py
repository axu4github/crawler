# -*- coding: utf-8 -*-
import scrapy
import time
from jd.items import JdItem
from scrapy.loader import ItemLoader

class jdSpider(scrapy.spiders.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ["http://item.jd.com/987695.html"]

    def parse(self, response):
        p = ItemLoader(item=JdItem(), response=response)
        p.add_xpath("id", "//div[@id='product-intro']//div[@id='short-share']//span[1]")
        p.add_xpath("name", "//div[@id='itemInfo']//div[@id='name']/h1")
        p.add_xpath("price", "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-price']//strong[@id='jd-price']")
        p.add_xpath("seller", "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-service']//div[@class='dd']")
        # p.add_xpath("prompts", "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']")
        p.add_xpath("classification", "//div[@id='root-nav']//div[@class='breadcrumb']/strong/a/text()")
        p.add_xpath("brand", "//div[@id='root-nav']//div[@class='breadcrumb']//span[2]/a[1]")
        p.load_item()

        print vars(p)

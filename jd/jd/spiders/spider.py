# -*- coding: utf-8 -*-
 
import scrapy
import time

class jdSpider(scrapy.spiders.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ["http://item.jd.com/2543762.html"]

    def parse(self, response):
        while True:
            print response.url
            time.sleep(5)

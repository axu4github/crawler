# -*- coding: utf-8 -*-
 
import scrapy
import time

class jdSpider(scrapy.spiders.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ["http://item.jd.com/2930658.html"]

    def parse(self, response):
        print "parse " + response.url

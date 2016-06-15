# -*- coding: utf-8 -*- 
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from scrapy.http import Response

# class DynamicResposne(Response):
#     def __init__(self):
#         Response.__init__(self)

class DynamicPageMiddleware(object):
    
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def __del__(self):
        self.driver.close()

    def process_response(self, request, response, spider):
        self.driver.get(request.url)
        return response.replace(body=self.driver.page_source)

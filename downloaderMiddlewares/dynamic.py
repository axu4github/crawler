# -*- coding: utf-8 -*- 
from selenium import webdriver
import time
import sys
reload(sys)                         
sys.setdefaultencoding('utf-8') 

class DynamicPageMiddleware(object):
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def process_response(self, request, response, spider):
        url = request.url
        self.driver.get(request.url)
        self.driver.implicitly_wait(10) # 隐式等待10秒
        # return response.replace(body=self.driver.page_source.encode('utf-8'))
        return response.replace(body=self.driver.page_source)

    def process_exception(self, request, exception, spider):
        self.driver.close()
        
# -*- coding: utf-8 -*- 
from selenium import webdriver
import time

class DynamicPageMiddleware(object):
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        self.driver.close()

    def process_response(self, request, response, spider):
        url = request.url
        # 若不是抓取连接则直接返回response
        if url not in spider.start_urls:
            return response
        else:   
            self.driver.get(request.url)
            time.sleep(10)
            return response.replace(body=self.driver.page_source.encode('utf-8'))

    def process_exception(self, request, exception, spider):
        self.driver.close()
        
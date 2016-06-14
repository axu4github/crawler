import scrapy
from scrapy.http import TextResponse 

class DynamicPageMiddleware(object):
    
    def process_response(self, request, response, spider):
        print "DynamicPageMiddleware " + response.url
        # response.newP = "123"
        return TextResponse(url="www.baidu.com")
    
        
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import urllib
import urllib2
import json

class JdPipeline(object):

    def process_item(self, item, spider):
        if item['price'] and item['id']:
            data = {'product': {}}
            data['product']['unique'] = item['id']
            data['product']['name'] = item['name']
            data['product']['url'] = item['url']
            data['product']['img'] = item['img']
            data['product']['provider'] = spider.provider

            data['price'] = item['price']
            url = 'http://127.0.0.1:8000/api/prices/'
            post_data = json.dumps(data)
            print post_data
            request = urllib2.Request(url, post_data)
            request.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(request)
            content = response.read()

            print content
            return item
        else:
            raise DropItem("Missing price or id in %s" % item)

# -*- coding: utf-8 -*-

import urllib
import re
from ispiders.common_spider import CommonSpider


class amazonSpider(CommonSpider):

    name = "amazon"
    allowed_domains = ["www.amazon.cn"]
    handle_httpstatus_list = [301, 302, 503]

    # '''
    #     例子: https://www.amazon.cn/s/rh=i%3Aaps%2Ck%3Aapple%2Cp_n_fulfilled_by_amazon%3A326314071&keywords=apple
    # '''

    item_setting = {
        'website': 'amazon',
        'description': 'amazon_search',
        'base_url': "https://www.amazon.cn/s/rh=i%3Aaps%2Ck%3Aapple%2Cp_n_fulfilled_by_amazon%3A326314071&keywords={keyword}&page=1&sort=review-rank",
        'rules': {
            'item_list': ["//div[contains(@id, 'atfResults')]/ul/li"],
            'item': {
                'id':       ["./@data-asin"],
                'name':     [".//div[contains(@class, 'a-row a-spacing-mini')]//h2/text()"],
                'url':      [".//div[contains(@class, 'a-spacing-base')]//a[contains(@class, 'a-link-normal')]/@href"],
                'img':      [".//div[contains(@class, 'a-spacing-base')]//a[contains(@class, 'a-link-normal')]/img/@src"],
                'price':    [".//div[contains(@class, 'a-row a-spacing-mini')]//span[contains(@class, 's-price')]/text()"],
            },
            'page': ["//span[@class='pagnRA']"],
        }
    }

    # def post_process_url(self, value, item):
    #     return "http:{value}".format(value=value)

    # def post_process_img(self, value, item):
    #     return "http:{value}".format(value=value)

    # def post_process_name(self, value, item):
    #     return re.sub('<[^>]+>','',value)

    def post_parse(self, results):
        print len(results)
        i = 1
        for result in results:
            print "序号: %d, 编号: %s, 名称: %s, 价格: %s" % (i, result['id'], result['name'], result['price'])
            i += 1  

    #     # return results

    def get_next_page_url(self, response, curr_page_num):
        return "http://www.amazon.cn%s" % self._first(response.xpath("//span[@class='pagnRA']/a/@href").extract())
        # return url

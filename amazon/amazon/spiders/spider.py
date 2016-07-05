# -*- coding: utf-8 -*-

import urllib
import re
from ispiders.common_spider import CommonSpider


class amazonSpider(CommonSpider):

    name = "amazon"
    allowed_domains = ["www.amazon.cn"]
    handle_httpstatus_list = [301, 302]

    # '''
    #     京东商品列表url参数说明

    #     例子: https://www.amazon.cn/s/rh=i%3Aaps%2Ck%3Aapple%2Cp_n_fulfilled_by_amazon%3A326314071&keywords=apple
    #     说明:
    #         keyword: 关键字 (搜索内容)
    #         enc: 编码 (utf-8)
    #         stock:  是否选择京东配送
    #                 0 => 不选 京东配送
    #                 1 => 选择 京东配送 (非0均可)
    #         wtype:  是否选择显示有货
    #                 0 => 不选 显示有货
    #                 1 => 选择 显示有货 (非0均可)
    #         psort:  排序方式
    #                 0 => 按综合排序
    #                 1 => 按价格排序 （降序）
    #                 2 => 按价格排序 （升序）
    #                 3 => 按销量排序
    #                 4 => 按评论数排序
    #                 5 => 按新品排序
    #         page: 分页 (奇数 1,3,5,...,2n-1)
    # '''

    item_setting = {
        'website': 'amazon',
        'description': 'amazon_search',
        'base_url': "https://www.amazon.cn/s/rh=i%3Aaps%2Ck%3Aapple%2Cp_n_fulfilled_by_amazon%3A326314071&keywords={keyword}&page=1",
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
            print i
            i += 1
            for k, v in result.items():
                print "%s:%s" % (k,v)            

    #     # return results

    def get_next_page_url(self, response, curr_page_num):
        print " url ==========------------> %s " % response.url
        url = "http://www.amazon.cn%s" % self._first(response.xpath("//span[@class='pagnRA']/a/@href").extract())


        print "next url ==========------------> %s " % url

        return url

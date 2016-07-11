# -*- coding: utf-8 -*-

import urllib
import re
from ispiders.common_spider import CommonSpider


class jdSpider(CommonSpider):

    name = "jd"
    allowed_domains = ["jd.com"]

    # '''
    #     京东商品列表url参数说明

    #     例子: http://search.jd.com/Search?keyword=apple&enc=utf-8&stock=1&wtype=1&psort=3&page=1
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

    # 京东获取商品价格URL模板
    GET_ITEM_PRICE_URL_PATTERN = "http://p.3.cn/prices/mgets?skuIds=J_{item_id}&type=1"

    item_setting = {
        'website': 'jd',
        'description': 'jd_search',
        'base_url': 'http://search.jd.com/Search?keyword={keyword}&enc=utf-8&stock=1&wtype=1&psort=3',
        'page_url': '{base_url}&page={page}',
        'item_class': 'JdItem',
        'rules': {
            'item_list': ["//div[contains(@id, 'J_goodsList')]/ul/li"],
            'item': {
                'id':       ["./@data-sku"],
                'name':     [".//div[contains(@class, 'p-name')]/a/em"],
                'url':      [".//div[contains(@class, 'p-name')]/a/@href"],
                'img':      [".//div[contains(@class, 'p-img')]/a/img/@src", ".//div[contains(@class, 'p-img')]/a/img/@data-lazy-img"],
                'price':    [".//div[contains(@class, 'p-price')]//i/text()"],
            },
            'page': ["//a[contains(@class, 'fp-next')]/@onclick"],
        }
    }

    def post_process_url(self, value, item):
        return "http:{value}".format(value=value)

    def post_process_img(self, value, item):
        return "http:{value}".format(value=value)

    def post_process_name(self, value, item):
        return re.sub('<[^>]+>','',value)

    def get_next_page_url(self, response, curr_page_num):
        arr_base_url = response.url.split('?')
        page_number = int(response.xpath(self.item_setting['rules']['page'][
                          0]).extract()[0].split('(').pop().split(')')[0])
        # 提取参数，并将其转化为k=>v数组
        argus = {item.split('=')[0]: item.split('=')[1]
                 for item in arr_base_url.pop().split('&')}
        if page_number:
            argus['page'] = page_number

        return "{base_url}?{arguments}".format(base_url=arr_base_url[0], arguments=urllib.urlencode(argus))

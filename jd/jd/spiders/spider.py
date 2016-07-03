# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import time
import urllib
import json
from jd.items import JdItem
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from scrapy.http import Request
from ispiders.common_spider import CommonSpider


class jdSpider(CommonSpider):

    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = []
    current_page_number = 1
    result_set = []

    '''
        京东商品列表url参数说明

        例子: http://search.jd.com/Search?keyword=apple&enc=utf-8&stock=1&wtype=1&psort=3&page=1
        说明: 
            keyword: 关键字 (搜索内容)
            enc: 编码 (utf-8)
            stock:  是否选择京东配送
                    0 => 不选 京东配送 
                    1 => 选择 京东配送 (非0均可)
            wtype:  是否选择显示有货
                    0 => 不选 显示有货 
                    1 => 选择 显示有货 (非0均可)
            psort:  排序方式
                    0 => 按综合排序
                    1 => 按价格排序 （降序）
                    2 => 按价格排序 （升序）
                    3 => 按销量排序
                    4 => 按评论数排序
                    5 => 按新品排序
            page: 分页 (奇数 1,3,5,...,2n-1)
    '''
    # 搜索URL模板
    SEARCH_URL_PATTERN = "http://search.jd.com/Search?keyword={keyword}&enc={enc}&stock={stock}&wtype={wtype}&psort={psort}"
    # 搜索URL默认参数
    DEFAULT_ENC = 'utf-8'  # 网页编码
    DEFAULT_STOCK = 1  # 选择京东配送（京东自营）
    DEFAULT_WTYPE = 1  # 选择有货
    DEFAULT_PSORT = 3  # 按照销量排序
    DEFAULT_PAGE = 1  # 第一页
    # 搜索关键字
    KEY_WORDS = [
        'apple',
        # '苹果配件',
    ]
    # 京东获取商品价格URL模板
    GET_ITEM_PRICE_URL_PATTERN = "http://p.3.cn/prices/mgets?skuIds=J_{item_id}&type=1"
    MAX_PAGE = 3

    # 分页URL模板
    PAGE_URL_PATTERN = "{search_url}&page={page}"

    # 初始化 加载 start_urls 内容
    def __init__(self, *args, **kwargs):
        super(jdSpider, self).__init__(*args, **kwargs)
        self.init_start_urls()

    def init_start_urls(self):
        for keyword in self.KEY_WORDS:
            if keyword:
                self.start_urls.append(self.SEARCH_URL_PATTERN.format(
                    keyword=keyword,
                    enc=self.DEFAULT_ENC,
                    stock=self.DEFAULT_STOCK,
                    wtype=self.DEFAULT_WTYPE,
                    psort=self.DEFAULT_PSORT
                ))

    def get_item_price_by_request(self, item_id):
        item_price = urllib.urlopen(
            self.GET_ITEM_PRICE_URL_PATTERN.format(item_id=item_id)).read()
        return json.loads(item_price)[0]['p']

    def process_item(self, items):
        for item in items:
            item_id = item.xpath("./@data-sku").extract()[0]
            item_name = item.xpath(
                ".//div[contains(@class, 'p-name')]/a/@title").extract()[0]
            item_url = "http:%s" % item.xpath(
                ".//div[contains(@class, 'p-name')]/a/@href").extract()[0]
            item_img = item.xpath(
                ".//div[contains(@class, 'p-img')]/a/img/@src").extract()
            if len(item_img) == 0:
                item_img = item.xpath(
                    ".//div[contains(@class, 'p-img')]/a/img/@data-lazy-img").extract()
            item_price = self.get_item_price_by_request(item_id)
            self.result_set.append({
                'id': item_id,
                'name': item_name,
                'url': item_url,
                'img': item_img,
                'price': item_price
            })


    def parse(self, response):
        self.process_item(response.xpath(
            "//div[contains(@id, 'J_goodsList')]//li"))
        next_page = response.xpath(
            "//a[contains(@class, 'fp-next')]/@onclick").extract()
        if next_page and self.current_page_number <= self.MAX_PAGE:
            page_number = int(next_page[0].split('(').pop().split(')')[0])
            self.current_page_number += 1
            return scrapy.Request(self.get_next_page_url(response.url, page_number), callback=self.parse)

        print len(self.result_set)
        return self.result_set

    def get_next_page_url(self, url, page_number):
        arr_base_url = url.split('?')
        # 提取参数，并将其转化为k=>v数组
        argus = {item.split('=')[0]: item.split('=')[1]
                 for item in arr_base_url.pop().split('&')}
        if page_number:
            argus['page'] = page_number

        return "{base_url}?{arguments}".format(base_url=arr_base_url[0], arguments=urllib.urlencode(argus))

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


class jdSpider(Spider):

    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = []

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
    SEARCH_URL_PATTERN = "http://search.jd.com/Search?keyword={keyword}&enc={enc}&stock={stock}&wtype={wtype}&psort={psort}&page={page}"
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

    itemOfSelfEmployed = {
        "id": {"xpath": "//div[@id='product-intro']//div[@id='short-share']//span[2]/text()"},
        "name": {"xpath": "//div[@id='itemInfo']//div[@id='name']/h1/text()"},
        "price": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-price']//strong[@id='jd-price']/text()"},
        "seller": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='summary-service']//div[@class='dd']/text()"},
        # "prompts": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']/text()"},
        "classification": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']/strong/a/text()"},
        "brand": {"xpath": "//div[@id='root-nav']//div[@class='breadcrumb']//span[2]/a[1]/text()"},
    }

    itemOfOther = {
        "id": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='preview-info']//div[@class='sku']/span/text()"},
        "name": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='itemInfo-wrap']//div[@class='sku-name']/text()"},
        "price": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='itemInfo-wrap']//span[@class='p-price']/span/text()"},
        "seller": {"xpath": "//div[contains(@class, 'product-intro')]//div[@class='summary-stock']//div[@class='dd']//div[@class='summary-service']/descendant::text()"},
        # "prompts": {"xpath": "//div[@id='itemInfo']//div[@id='summary']//div[@id='J-summary-top']//em[@class='hl_red']/text()"},
        "classification": {"xpath": "//div[@class='crumb-wrap']//div[contains(@class, 'item')]/a[contains(@clstag, 'mbNav-1')]/text()"},
        "brand": {"xpath": "//div[@class='crumb-wrap']//div[contains(@class, 'item')]/a[contains(@clstag, 'mbNav-4')]/text()"},
    }

    # 初始化 加载 start_urls 内容
    def __init__(self, *args, **kwargs):
        super(jdSpider, self).__init__(*args, **kwargs)
        self.init_start_urls()
        print("====>%s<====" % '\n'.join(self.start_urls))

    def init_start_urls(self):
        for keyword in self.KEY_WORDS:
            if keyword:
                self.start_urls.append(self.SEARCH_URL_PATTERN.format(
                    keyword=keyword,
                    enc=self.DEFAULT_ENC,
                    stock=self.DEFAULT_STOCK,
                    wtype=self.DEFAULT_WTYPE,
                    psort=self.DEFAULT_PSORT,
                    page=self.DEFAULT_PAGE
                ))

    # 判断商品是不是京东自营
    def isSelfEmployed(self, response):
        return bool(response.xpath("//em[@class='u-jd']"))

    # 判断是否搜到商品
    def has_result(self, response):
        return bool(response.xpath("//div[contains(@id, 'J_goodsList')]"))

    def get_item_price_by_request(self, item_id):
        item_price = urllib.urlopen(self.GET_ITEM_PRICE_URL_PATTERN.format(item_id=item_id)).read()
        return json.loads(item_price)[0]['p']

    def process_item(self, items):
        for item in items:
            item_id = item.xpath("./@data-sku").extract()[0]
            item_name = item.xpath(".//div[contains(@class, 'p-name')]/a/@title").extract()[0]
            item_url = "http:%s" % item.xpath(".//div[contains(@class, 'p-name')]/a/@href").extract()[0]
            item_img = item.xpath(".//div[contains(@class, 'p-img')]/a/img/@src").extract()
            if len(item_img) == 0:
                item_img = item.xpath(".//div[contains(@class, 'p-img')]/a/img/@data-lazy-img").extract()
            # item_price = item.xpath(".//div[contains(@class, 'p-price')]/strong/@data-price").extract()
            # item_price = ''
            # if item_price: 
            item_price = self.get_item_price_by_request(item_id)

            print "| ==========="
            print "| 商品编号: %s" % item_id
            print "| 商品名称: %s" % item_name
            print "| 商品价格: %s" % item_price
            print "| 商品URL: %s" % item_url
            print "| 商品图片: %s" % item_img
            print "| ==========="

    def parse(self, response):
        if self.has_result(response):
            items = response.xpath("//ul[contains(@class, 'gl-warp')]/li")
            total_pages = int(response.xpath("//div[contains(@id, 'J_topPage')]/span[contains(@class, 'fp-text')]/i/text()").extract()[0])
            self.process_item(items)
            # for i in range(1, total_pages + 1, 2):
            #     # Request




    def parse_more_page(self, response):
        pass

    def parse_detail(self, response):
        self.item = self.itemOfSelfEmployed if self.isSelfEmployed(
            response) else self.itemOfOther

        p = ItemLoader(item=JdItem(), response=response)
        for key in self.item:
            p.add_xpath(key, self.item[key]["xpath"])

        p.load_item()
        print "| ==========="
        print "| 商品编号: %s" % "".join(p.get_output_value('id'))
        print "| 商品名称: %s" % "".join(p.get_output_value('name'))
        print "| 商品价格: %s" % "".join(p.get_output_value('price'))
        print "| 供应商: %s" % "".join(p.get_output_value('seller'))
        # print "| 促销信息: %s" % "+".join(p.get_output_value('prompts'))
        print "| 分类: %s" % "".join(p.get_output_value('classification'))
        print "| 品牌: %s" % "".join(p.get_output_value('brand'))
        print "| ==========="

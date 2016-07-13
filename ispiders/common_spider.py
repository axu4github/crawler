# -*- coding: utf-8 -*-
#
import scrapy


class CommonSpider(scrapy.Spider):
    '''
    通用Spider
    '''
    name = 'common_spider'
    start_urls = []
    # keywords = ['apple', 'beats', 'beo', 'bose 123']
    # keywords = ['apple', 'beats', '小米', '罗技', 'Bose', '微软', 'Jabra', 'FILCO']
    keywords = ['apple']
    results = []
    curr_page_num = 1
    max_page_num = 5

    def __init__(self, *args, **kwargs):
        super(CommonSpider, self).__init__(*args, **kwargs)
        self.init_start_urls()

    def init_start_urls(self):
        self.start_urls = [self.item_setting['base_url'].format(
            keyword=keyword) for keyword in self.keywords]

    # 处理产品列表
    def process_items(self, response):
        items = []
        list_rule = self._list(self.item_setting['rules']['item_list'])
        for lr in list_rule:
            for item in response.xpath(lr):
                items.append(self.process_item(item))

        return items

    # 处理单个产品
    def process_item(self, item):
        item_obj = {}
        for item_attr, item_xpaths in self.item_setting['rules']['item'].items():
            item_value = ""
            # 如果存在 process_{属性} 的方法，则优先执行该方法来获取该属性的值
            try:
                process_function = "process_{item_attr}".format(
                    item_attr=item_attr)
                item_value = getattr(self, process_function)(item)
            # 如果不存在 process_{属性} 的方法，则使用xpath
            except Exception, e:
                item_xpaths = self._list(item_xpaths)
                for item_xpath in item_xpaths:
                    item_xpath_value = item.xpath(item_xpath).extract()
                    if item_xpath_value:
                        item_value = self._first(item_xpath_value)
                        break
            finally:
                item_obj[item_attr] = item_value

            try:
                post_process_function = "post_process_{item_attr}".format(
                    item_attr=item_attr)
                item_value = getattr(
                    self, post_process_function)(item_value, item)
            except Exception, e:
                pass
            finally:
                item_obj[item_attr] = item_value

        # print item
        # for k, v in item_obj.items():
        #     print "%s:%s" % (k,v)

        return item_obj

    def has_next_page(self, response):
        if 'page' in self.item_setting['rules']:
            page_rules = self._list(self.item_setting['rules']['page'])
            for page_rule in page_rules:
                if response.xpath(page_rule).extract():
                    return True

        return False

    def parse(self, response):
        print "RESPOSNE URL ===========> %s <===========" % response.url
        self.results.extend(self.process_items(response))
        if self.has_next_page(response) and self.curr_page_num < self.max_page_num:
            next_page_url = self.get_next_page_url(
                response, self.curr_page_num)
            self.curr_page_num += 1
            return scrapy.Request(next_page_url, callback=self.parse)

        return self.post_parse(self.results)

    def post_parse(self, results):
        return results

    def _list(self, item):
        return item if type(item) == list else [item]

    def _first(self, item):
        return item if type(item) != list else item[0]

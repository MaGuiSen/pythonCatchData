# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealstartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IPItem(scrapy.Item):
    ip = scrapy.Field()
    address = scrapy.Field()
    port = scrapy.Field()
    ip_type = scrapy.Field()
    # 用于在pipeline里面进行判断用于那种解析方法
    pipeline_type = scrapy.Field()
    pass

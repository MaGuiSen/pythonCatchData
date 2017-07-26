# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContentItem(scrapy.Item):
    title = scrapy.Field()
    post_date = scrapy.Field()
    summary = scrapy.Field()
    keywords = scrapy.Field()
    image_urls = scrapy.Field()
    source_url = scrapy.Field()
    content_type = scrapy.Field()  # news video
    content_html = scrapy.Field()
    styles = scrapy.Field()
    hash_code = scrapy.Field()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Spider, Request, Selector
from ..utils import query_params, gen_request_uuid
import json, time, scrapy, logging


class HKETLList(Spider):
    """
    香港etl列表: 'http://hk.morningstar.com/ap/etf/Explore.aspx?Type=4'
    """
    name = "us-etf-list"
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    allowed_domains = ["hk.morningstar.com", "gllt.morningstar.com", "news.morningstar.com"]
    start_urls = [
        'http://news.morningstar.com/etf/Lists/ETFReturns.html']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'page': 1}, callback=self.parse_entry_page)

    def parse_entry_page(self, response):
        form_data = {'curField': '3',
                     'curD': '1|1|1|-1|1|1|1|1|1||',
                     'firstRecNum': '0',
                     'lastRecNum': '2000',
                     'sortColumn': '0',
                     'category': '0',
                     'topNum': 'All'}
        next_req = scrapy.FormRequest(url='http://news.morningstar.com/etf/Lists/ETFReturns.html', callback=self.parse,
                                      formdata=form_data)
        yield next_req

    def parse(self, response):
        selector = Selector(response)

        xp = '/html/body/div/div[3]/div/table[3]/tr'
        items_tr = selector.xpath(xp)
        request_id = gen_request_uuid()
        results = []
        items_num = len(items_tr)
        for idx, item in enumerate(items_tr):
            # 排除前三个和最后一个
            if idx <= 2 or idx == items_num - 1:
                continue
            name = item.xpath('td[2]/a/text()').extract_first()
            quote_url = item.xpath('td[2]/a/@href').extract_first()
            category = item.xpath('td[3]/text()').extract_first()
            stylebox = item.xpath('td[4]/img/@src').extract_first()
            if stylebox is not None:
                #logging.debug(stylebox)
                stylebox = stylebox[-5:-4]

            params = query_params(quote_url) if quote_url is not None else {}

            if 'ticker' not in params:
                logging.info("erroe on parse item %s", name)
            item_result = {
                'request_id': request_id,
                'fund_name': name,
                'fund_quote_url': quote_url,
                'category': category,
                'stylebox': stylebox,
                'ticker': params['ticker'] if 'ticker' in params else None,
                'from_url': response.url,
                'crawl_time': time.strftime(self.ISOTIMEFORMAT, time.localtime())
            }
            results.append(item_result)

        yield {
            'item_type': 'us_etl_list',
            'item_list': results
        }

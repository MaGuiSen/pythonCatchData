#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Spider, Request, Selector
from ..utils import query_params, gen_request_uuid
import json, time, scrapy, logging


class HKETLList(Spider):
    """
    香港etl列表: 'http://hk.morningstar.com/ap/etf/Explore.aspx?Type=4'
    """
    name = "cn-etf-list"
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    allowed_domains = ["hk.morningstar.com", "gllt.morningstar.com", "cn.morningstar.com"]
    start_urls = [
        'https://cn.morningstar.com/etf/quickrank.aspx?group=ET']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'page': 1})

    def parse(self, response):
        #logging.info(response.body)
        selector = Selector(response)
        xp = '//*[@id="ctl00_cphMain_gridResult"]/tr[contains(@class,"grid")]'
        items_tr = selector.xpath(xp)
        request_id = gen_request_uuid()
        results = []
        for item in items_tr:
            fund_code = item.xpath('td[1]/a/text()').extract_first()
            name = item.xpath('td[2]/a/text()').extract_first()
            relative_url = item.xpath('td[2]/a/@href').extract_first();
            detail_url = 'https://cn.morningstar.com' + relative_url
            ms_id = relative_url.split('/')[-1]
            category = item.xpath('td[3]/text()').extract_first()
            purchase_status = item.xpath('td[4]/text()').extract_first()
            redemption_status = item.xpath('td[5]/text()').extract_first()
            ms_3yr_rate = item.xpath('td[6]/img/@src').extract_first()[-10:-9]
            ms_5yr_rate = item.xpath('td[7]/img/@src').extract_first()[-10:-9]
            found_date = item.xpath('td[8]/text()').extract_first()

            item_result = {
                'request_id': request_id,
                'fund_name': name,
                'fund_code': fund_code,
                'fund_detail_url': detail_url,
                'pid': ms_id,
                'category': category,
                'purchase_status': purchase_status,
                'redemption_status': redemption_status,
                'ms_3yr_rate': ms_3yr_rate,
                'ms_5yr_rate': ms_5yr_rate,
                'found_date': found_date,
                'from_url': response.url,
                'crawl_time': time.strftime(self.ISOTIMEFORMAT, time.localtime())
            }
            results.append(item_result)

        logging.info("tr num %s", len(items_tr))
        logging.info("scraped %s items from page %s", len(results), response.meta['page'])
        yield {
            'item_type': 'cn_etl_list',
            'item_list': results
        }

        if response.meta['page'] == 1:
            page_links = selector.xpath('//*[@id="ctl00_cphMain_AspNetPager1"]/a')
            page_info_str = selector.xpath(
                '//*[@id="ctl00_cphMain_AspNetPager1"]/a[' + str(len(page_links)) + ']/@href').extract_first()
            total_page = self.extract_total_page(page_info_str)
            logging.info("total %s pages", total_page)

            next_page = response.meta['page'] + 1
            if next_page <= total_page:
                form_data = {'__EVENTTARGET': 'ctl00$cphMain$AspNetPager1',
                             '__EVENTARGUMENT': str(next_page)}
                next_req = scrapy.FormRequest.from_response(response, formnumber=0, formdata=form_data, dont_click=True)
                yield next_req.replace(meta={'page': next_page, 'total_page': total_page})
        else:
            next_page = response.meta['page'] + 1
            total_page = response.meta['total_page']
            if next_page <= total_page:
                form_data = {'__EVENTTARGET': 'ctl00$cphMain$AspNetPager1',
                             '__EVENTARGUMENT': str(next_page)}
                next_req = scrapy.FormRequest.from_response(response, formnumber=0, formdata=form_data, dont_click=True)
                yield next_req.replace(meta={'page': next_page, 'total_page': total_page})
        logging.info("finished page [%s]", response.meta['page'])

    @staticmethod
    def extract_total_page(page_info_str):
        total_num_str = page_info_str.split(',')[1].strip()[1:-2]
        return int(total_num_str)

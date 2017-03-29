#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Spider, Request, Selector
from ..utils import query_params, gen_request_uuid
import json, time, scrapy, logging


class HKETLList(Spider):
    """
    香港etl列表: 'http://hk.morningstar.com/ap/etf/Explore.aspx?Type=4'
    """
    name = "hk-etf-list"
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    allowed_domains = ["hk.morningstar.com", "gllt.morningstar.com"]
    start_urls = [
        'https://gllt.morningstar.com/roq2rh8blz/etfquickrank/default.aspx?Universe=ETALL%24%24ALL&tab=Performance&sortby=ReturnM0&LanguageId=en-GB']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, meta={'page': 1})

    def parse(self, response):
        selector = Selector(response)

        xp = '//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_gridResult"]/tr[contains(@class,"gridItem")]'
        items_tr = selector.xpath(xp)
        request_id = gen_request_uuid()
        results = []
        for item in items_tr:
            name = item.xpath('td[2]/a/text()').extract_first()
            detail_url = item.xpath('td[2]/a/@href').extract_first()
            detail_url = 'https://gllt.morningstar.com/roq2rh8blz' + detail_url[2:]
            on_click = item.xpath('td[1]/input/@onclick').extract_first()
            prop_start = on_click.index('{')
            prop_end = on_click.index('}') + 1
            prop_json_str = on_click[prop_start:prop_end]
            prop = json.loads(prop_json_str.replace("\\", ""))

            param_prop = query_params(detail_url)

            item_result = {
                'request_id': request_id,
                'fund_name': name,
                'fund_detail_url': detail_url,
                'isin': prop['isin'],
                'pid': prop['performanceid'],
                'symbol': prop['symbol'],
                'security_token': prop['securitytoken'],
                'ms_fund_id': prop['fundid'],
                'currency_id': param_prop['CurrencyId'],
                'base_currency_id': param_prop['BaseCurrencyId'],
                'from_url': response.url,
                'crawl_time': time.strftime(self.ISOTIMEFORMAT, time.localtime())
            }
            results.append(item_result)

        yield {
            'item_type': 'hk_etl_list',
            'item_list': results
        }

        if response.meta['page'] == 1:
            page_info_str = selector.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_aFundQuickrankControl_AspNetPager"]/table/tr/td[1]/span/text()').extract_first()
            total_page = self.extract_total_page(page_info_str)
            logging.info("total %s pages", total_page)

            next_page = response.meta['page'] + 1
            if next_page <= total_page:
                form_data = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$aFundQuickrankControl$AspNetPager',
                             '__EVENTARGUMENT': str(next_page)}
                next_req = scrapy.FormRequest.from_response(response, formnumber=0, formdata=form_data, dont_click=True)
                yield next_req.replace(meta={'page': next_page, 'total_page': total_page})
        else:
            next_page = response.meta['page'] + 1
            total_page = response.meta['total_page']
            if next_page <= total_page:
                form_data = {'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$aFundQuickrankControl$AspNetPager',
                             '__EVENTARGUMENT': str(next_page)}
                next_req = scrapy.FormRequest.from_response(response, formnumber=0, formdata=form_data, dont_click=True)
                yield next_req.replace(meta={'page': next_page, 'total_page': total_page})
        logging.info("finished page [%s]", response.meta['page'])

    @staticmethod
    def extract_total_page(page_info_str):
        total_num = int(page_info_str.split('of')[1].strip())
        page_begin, page_end = (int(p) for p in page_info_str.split('of')[0].split('-'))
        page_size = page_end - page_begin + 1
        basic_page_num = total_num / page_size
        remain = total_num % page_size
        return basic_page_num if remain == 0 else basic_page_num + 1

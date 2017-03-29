# -*- coding: UTF-8 -*-
from scrapy import Selector, Request, Spider
from ..utils import query_params, gen_request_uuid
from scrapy.exceptions import CloseSpider
import json, time, scrapy, logging


class HkCnaNews(Spider):
    name = 'hk-cna-news'
    allowed_domain = ["hkcna.hk"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    headers = {'User-Agent': user_agent}

    start_urls = [
        'http://www.hkcna.hk/m/scroll.html'
    ]

    def parse(self, response):
        sel = Selector(response)
        info = sel.xpath('//ul[@class="w-list"]/li')
        if len(info) == 0:
            raise CloseSpider('---------------------End Search!---------------')

        for item in info:
            title = item.xpath('a/text()').extract_first()
            date = item.xpath('span/text()').extract_first().encode('utf-8')

            detail_url = item.xpath('a/@href').extract_first().encode('utf-8')
            detail_url = detail_url if detail_url.startswith('http') else 'http://www.hkcna.hk' + detail_url
            result = {
                'item_type': 'hk_cna_news',
                'item_data': {
                    'title': title,
                    'news_date': int(time.mktime(time.strptime(date.replace('.', '-'), '%Y-%m-%d %H:%M'))),
                    'detail_url': detail_url,
                    'create_at': int(time.time())
                }
            }
            yield scrapy.Request(url=detail_url, meta={'item': result}, callback=self.parseDetail)

        url = response.url.split('_')
        if len(url) == 1:
            next_url = 'http://www.hkcna.hk/m/scroll_2.html'
        else:
            index = int(url[1].split('.')[0]) + 1;
            next_url = url[0]+ '_' + str(index) + '.html';

        yield scrapy.Request(url=next_url, callback=self.parse)

    def parseDetail(self, response):
        sel = Selector(response)
        data = response.meta['item']
        info = sel.xpath('//*[@id="mai_bj"]/div[1]/div')
        # body_attr = self.getNewsSomeThing(info.extract_first().encode('utf-8'))
        body_text = str(info.extract_first().encode('utf-8'))
        contents, source, editor = self.getNewsSomeThing(body_text)
        data['item_data']['body'] = contents
        data['item_data']['source'] = source
        data['item_data']['editor'] = editor
        return data

    def getNewsSomeThing(self, body):
        """
        获取新闻body内的内容，发布时间，和编辑人员
        :param body:
        :return:
        """
        selectors = Selector(text=body)
        # 内容，以\n分段
        contents = selectors.xpath('//p/text()').extract()
        contents = '\n'.join(contents).replace(u'　', '')
        # 来源及发布时间 2017年02月08日 11:18 稿件来源：中新網
        source = selectors.xpath('//div[@class="tm"]/text()').extract()
        source = ''.join(source).replace(u'  ', u' ')
        # 编辑的人
        editor = selectors.xpath('//div[@class="fdr"]/span/text()').extract()
        editor = ''.join(editor)
        print contents
        print source
        print editor
        return contents, source, editor

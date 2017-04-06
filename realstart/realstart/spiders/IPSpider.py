# -*- coding: utf-8 -*-
import scrapy
from ..items import IPItem
from bs4 import BeautifulSoup
from .. import contanst


class IPSpider(scrapy.Spider):
    name = 'crawl_ip'

    def closed(self, response):
        # 当spider关闭时，该函数被调用。 该方法提供了一个替代调用signals.connect()来监听 spider_closed 信号的快捷方式。
        print "spider close"
        contanst.ip_spider_status = 'stop'

    def start_requests(self):
        urls = [
            'http://www.xicidaili.com/',
        ]
        for url in urls:
            print u'请求url：' + url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print u'开始解析。。。'
        page = BeautifulSoup(response.body, 'lxml')
        ipItem = IPItem()
        ipTrs = page.select('#ip_list tr')
        for ipTr in ipTrs:
            ipTds = ipTr.select('td')
            if len(ipTds) < 8:
                continue
            ipItem['ip'] = ipTds[1].get_text()
            if not ipItem['ip'] or ipItem['ip'] == u'代理IP地址':
                continue
            ipItem['port'] = ipTds[2].get_text()
            ipItem['address'] = ipTds[3].get_text()
            ipItem['ip_type'] = ipTds[5].get_text()
            ipItem['pipeline_type'] = 'IPItem'
            if ipItem['ip_type'] != u'HTTP':
                continue
            # 存到数据库
            yield ipItem
        pass

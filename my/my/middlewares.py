# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

from scrapy import signals

class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # mysql_host=crawler.settings.get('MYSQL_HOST'),
            # mysql_user=crawler.settings.get('MYSQL_USER'),
            # mysql_passwd=crawler.settings.get('MYSQL_PASSWD'),
            # mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def process_request(self, request, spider):
        print ("dddddddddddddddddddddddddddddddddddddd2222222222222")
        # try:
        #     self.conn = MySQLdb.connect(
        #         user=self.mysql_user,
        #         passwd=self.mysql_passwd,
        #         db=self.mysql_db,
        #         host=self.mysql_host,
        #         charset="utf8",
        #         use_unicode=True
        #     )
        #     self.cursor = self.conn.cursor()
        # except MySQLdb.Error, e:
        #     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        # self.cursor.execute(
        #     'SELECT * FROM xicidaili order by verified_time DESC Limit 0,10')
        # proxy_item = self.cursor.fetchall()
        # proxy = random.choice(proxy_item)
        # user_pass = proxy[4]
        # ip = proxy[1]
        # port = proxy[2]
        # http_method = proxy[6]
        # http_method = http_method.lower()
        # if user_pass is not None:
        #     request.meta['proxy'] = "%s://%s:%s" % (http_method, ip, port)
        #     encoded_user_pass = base64.encodestring(user_pass)
        #     request.headers[
        #         'Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        # else:
        request.meta['proxy'] = "%s://%s:%s" % ("http", "171.121.158.113", "808")

    def process_spider_exception(response, exception, spider):
            # Called when a spider or process_spider_input() method
            # (from other spider middleware) raises an exception.

            # Should return either None or an iterable of Response, dict
            # or Item objects.
            print ('+++MySpiderMiddleware_process_spider_exception')
            pass


class MySpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        print ('+++MySpiderMiddleware_from_crawler')
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        print ('+++MySpiderMiddleware_process_spider_input')
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        print ('+++MySpiderMiddleware_process_spider_output')
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        print ('+++MySpiderMiddleware_process_spider_exception')
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        print ('+++MySpiderMiddleware_process_start_requests')
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        # spider.logger.info('Spider opened: %s' % spider.name)
        pass

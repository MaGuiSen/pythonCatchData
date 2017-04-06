# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

import MySQLdb
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
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_pwd):
        print '#### ProxyMiddleware __init__ ####'
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_pwd = mysql_pwd

    @classmethod
    def from_crawler(cls, crawler):
        print '#### ProxyMiddleware from_crawler ####'
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_pwd=crawler.settings.get('MYSQL_PWD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def process_request(self, request, spider):
        print '#### ProxyMiddleware process_request ####'
        # 这边设置代理
        # request.meta['proxy'] = "%s://%s:%s" % ('http', '203.70.11.186', '80')
        # try:
        #     self.conn = MySQLdb.connect(
        #         user=self.mysql_user,
        #         passwd=self.mysql_pwd,
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
        #     request.meta['proxy'] = "%s://%s:%s" % (http_method, ip, port)

    def process_response(self, request, response, spider):
        print response.status
        print '#### ProxyMiddleware process_response ####'
        return response
        # 这边根据response的status判断是正常的还是ip被禁止了，然后根据类型返回response或者是再次执行request

    def process_exception(self, request, exception, spider):
        print exception
        print '#### ProxyMiddleware process_exception ####'
        # 这边判断 错误类型，根据错误类型返回request，让他继续执行
        # return request //这个如果返回request，那么异常之后还会继续之前的请求，会出现死循环


class SpiderOutputMiddleware(object):
    def process_spider_output(self, response, result, spider):
        print ("#### SpiderOutputMiddleware process_spider_output ####")
        return result

    def process_spider_input(self, response, spider):
        # inspect_response(response, spider)
        print ("#### SpiderOutputMiddleware process_spider_input ####")
        return

    def process_start_requests(self, start_requests, spider):
        print ("#### SpiderOutputMiddleware process_start_requests ####")
        last_request = []
        for one_request in start_requests:
            last_request.append(one_request)
        return last_request

    def process_spider_exception(self, response, exception, spider):
        print (exception)
        print ("#### SpiderOutputMiddleware process_spider_exception ####")
        return


class RealstartSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

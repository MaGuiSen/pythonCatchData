# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json

from scrapy import signals


class MyCustomDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    # def process_request(slef,request, spider):
    #     print '+++++++++++process_request'
    #     return request
    def process_response(self, request, response, spider):
        print response.status
        return response

    def process_exception(self, request, exception, spider):
        print exception
        print '+++++++++++process_exception'
        # return request //这个如果返回request，那么异常之后还会继续之前的请求，会出现死循环

class SpiderOutputMiddleware(object):

    def process_spider_output(self, response, result, spider):
        print ("#### 1111111")
        return result

    def process_spider_input(self, response, spider):
        # inspect_response(response, spider)
        print ("#### 33333 ")
        return

    def process_start_requests(self, start_requests, spider):
        print ("#### 2222222 ")
        last_request = []
        for one_request in start_requests:
            last_request.append(one_request)
        return last_request

    def process_spider_exception(self,response, exception, spider):
        print (exception)
        print ("我啊啊啊啊 啊啊啊")
        return
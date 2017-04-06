# -*- coding: utf-8 -*-
from threading import Timer

from scrapy import cmdline

#
import contanst
from validator.validatorIP import validatorIP


def timerLaunch():
    if contanst.ip_spider_status is not 'running':
        contanst.ip_validator_status = 'running'
        cmdline.execute("scrapy crawl crawl_ip".split())
        # process = CrawlerProcess()
        # process.crawl(IPSpider)
        # process.start()
        pass
    if contanst.ip_validator_status is not 'running':
        contanst.ip_validator_status = 'running'
        val = validatorIP()
        isEnd = val.start()
        if isEnd:
            contanst.ip_validator_status = 'stop'
            print contanst.ip_validator_status

    Timer(10, timerLaunch).start()


timerLaunch()

# cmdline.execute("scrapy crawl crawl_ip".split())
# -*- coding: utf-8 -*-
import time

import contanst
from validator.validatorIP import validatorIP

#
# class scrapyThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         print "start ip scrapy"
#         if contanst.ip_spider_status is not 'running':
#             contanst.ip_validator_status = 'running'
#             cmdline.execute("scrapy crawl crawl_ip".split())
#
#
# class ipValidateThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         print "start ip validate"
#         if contanst.ip_validator_status is not 'running':
#             contanst.ip_validator_status = 'running'
#             val = validatorIP()
#             isEnd = val.start()
#             if isEnd:
#                 contanst.ip_validator_status = 'stop'
#                 print contanst.ip_validator_status
#
#
# def timerLaunch():
#     ipThread = ipValidateThread()
#     ipScrapyThread = scrapyThread()
#     ipThread.start()
#     ipScrapyThread.start()
#     print "timer--run"
#     Timer(10, timerLaunch).start()
#
#
# timerLaunch()

# cmdline.execute("scrapy crawl crawl_ip".split())

while True:
    print 'ip validate'
    if contanst.ip_validator_status is not 'running':
        contanst.ip_validator_status = 'running'
        val = validatorIP()
        isEnd = val.start()
        if isEnd:
            contanst.ip_validator_status = 'stop'
            print contanst.ip_validator_status
    time.sleep(20)

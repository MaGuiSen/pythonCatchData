# -*- coding: utf-8 -*-
import json
import time

import demjson
import scrapy
from scrapy import Selector

from libMe.util import CssUtil
from libMe.util import EncryptUtil
from zixun.items import ContentItem
from ..db.CheckDao import CheckDao
from libMe.util import EncodeUtil


class ZiXunSpider(scrapy.Spider):
    name = 'zixunDetail'

    def __init__(self, name=None, **kwargs):
        super(ZiXunSpider, self).__init__(name=None, **kwargs)
        self.count = 0
        self.request_stop = False
        self.request_stop_time = 0
        self.checkDao = CheckDao()
        # 用于缓存css
        self.css = {
            'hash': 'style'
        }

    def close(spider, reason):
        spider.saveStatus('stop')

    def start_requests(self):
        # 如果正在爬，就不请求
        status = self.getStatus()
        if status == 'running':
            return
        self.saveStatus('running')
        cookies ={'wuid_createAt': '2017-06-30 12:47:59', 'UM_distinctid': '15cf753c1ce41e-01a3b15fcaada1-4383666-100200-15cf753c1cf393', 'CNZZDATA1255169715': '359892489-1498797024-null%7C1501070424', 'wuid': '567120835966164', 'Hm_lvt_15fafbae2b9b11d280c79eff3b840e45': '1499861822,1500904156,1500989430,1501067829', 'captcha': 's%3A09685a3044a9a523ec779191971ae559.cSQoBtWi18ke52SSAYkRzvu4RmMrakOgQgFxeJpimYQ', 'cn_9a154edda337ag57c050_dplus': '%7B%22distinct_id%22%3A%20%2215cf753c1ce41e-01a3b15fcaada1-4383666-100200-15cf753c1cf393%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201501073081%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201501073081%2C%22%E6%9D%A5%E6%BA%90%E6%B8%A0%E9%81%93%22%3A%20%22%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221499857767%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D', 'Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45': '1501073083', 'JSESSIONID': '2ad86e161f283d233e71da3c062f07350257435a809e0fe4189cb72ebe5d6317', 'weather_auth': '2'}
        maxPage = 2
        for pageIndex in range(0, maxPage + 1):
            dataLong = time.time() * 1000
            # http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12413478388&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1501073082588
            url = 'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=12413478388&cstart=%d&cend=%d' \
                  '&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=%d' % (
                      pageIndex * 10, (pageIndex + 1) * 10, dataLong)
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        body = EncodeUtil.toUnicode(response.body)
        if False:
            pass
        else:
            # 格式化
            jsonStr = demjson.decode(body) or {}
            articles = jsonStr.get('result') or []
            for article in articles:
                default_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                title = article.get('title', '')
                post_date = article.get('date', default_time)
                summary = article.get('summary', '')
                keywords = article.get('keywords', [])
                source_url = article.get('url')
                content_type = article.get('content_type', 'news')  # news video
                image_urls = article.get('image_urls', [])
                if not title or not source_url or content_type == 'video':
                    continue
                # 如果存在则不抓取
                if self.checkDao.checkExist(source_url):
                    self.infoStr('已经存在')
                    continue
                # 得到hashCode
                hash_code = self.checkDao.getHashCode(source_url)
                contentItem = ContentItem()
                contentItem['title'] = title
                contentItem['post_date'] = post_date
                contentItem['summary'] = summary
                contentItem['keywords'] = ','.join(keywords)
                contentItem['source_url'] = source_url
                contentItem['content_type'] = content_type
                contentItem['hash_code'] = hash_code

                image_urls_new = []
                for image_url in image_urls:
                    if not image_url.startswith('http'):
                        image_url = 'http://i1.go2yd.com/image.php?type=thumbnail_336x216&url=%s' % image_url
                    image_urls_new.append(image_url)

                contentItem['image_urls'] = ','.join(image_urls_new)

                self.infoStr(u'抓取文章' + title + ':' + post_date + ':' + source_url)
                yield scrapy.Request(url=source_url,
                                     meta={'request_type': 'zixun_detail', "title": title,
                                           'contentItem': contentItem,
                                           "source_url": source_url},
                                     callback=self.parseArticle)

    def parseArticle(self, response):
        source_url = response.meta['source_url']
        body = EncodeUtil.toUnicode(response.body)
        if False:
            self.infoStr(u'访问过多被禁止')
        else:
            self.infoStr(u'开始解析界面')
            title = response.meta['title']
            source_url = response.meta['source_url']
            contentItem = response.meta['contentItem']
            selector = Selector(text=body)
            # 得到样式
            styleUrls = selector.xpath('//link[@rel="stylesheet"]/@href').extract()
            styleList = []
            for styleUrl in styleUrls:
                # 得到hash作为key
                styleUrlHash = EncryptUtil.md5(styleUrl)
                if not self.css.get(styleUrlHash):
                    # 不存在则去下载 并保存
                    if styleUrl.startswith('//static'):
                        styleUrl = 'http:'+styleUrl
                    self.css[styleUrlHash] = CssUtil.downLoad(styleUrl)
                styleList.append(self.css[styleUrlHash])

            styleIns = selector.xpath('//style/text()').extract()
            for style in styleIns:
                styleList.append(style)

            styles = CssUtil.compressCss(styleList).replace('\'', '"').replace('\\', '\\\\')
            styles = CssUtil.clearUrl(styles)
            contentItem['styles'] = styles
            content_html = selector.xpath('//*[@id="imedia-article"]')
            if len(content_html):
                contentItem['content_html'] = content_html.extract_first('')
                return contentItem

    def infoStr(self, value):
        self.logger.info(value)

    def getStatus(self):
        try:
            with open("catchStatus.json", 'r') as load_f:
                aa = json.load(load_f)
                return aa.get('status')
        finally:
            if load_f:
                load_f.close()

    def saveStatus(self, status):
        try:
            with open("catchStatus.json", "w") as f:
                json.dump({'status': status}, f)
        finally:
            if f:
                f.close()

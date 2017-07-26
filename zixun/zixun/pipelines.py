# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

from libMe.db.Connector import Connector
from .items import ContentItem


class MysqlPipeline(object):
    def __init__(self):
        self.connector = Connector()

    def process_item(self, item, spider):
        cursor = self.connector.cursor()
        if not cursor:
            return item
        if isinstance(item, ContentItem):
            # 如果存在，则不做处理
            spider.infoStr(u'存网易详情：' + item['title'])
            sql = "insert into zixun_detail (title,post_date,summary,keywords,image_urls,source_url,content_type,content_html,styles,hash_code,update_time) " \
                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            try:
                cursor.execute(sql, (
                    item['title'],
                    item['post_date'],
                    item['summary'],
                    item['keywords'],
                    item['image_urls'],
                    item['source_url'],
                    item['content_type'],
                    item['content_html'],
                    item['styles'],
                    item['hash_code'],
                    update_time))
                spider.infoStr(u'存详情：' + item['title'] + u'  成功' + u' ' + item['post_date'])
            except Exception, e:
                print e
                spider.infoStr(u'存详情：' + item['title'] + u'  失败')
                spider.infoStr(e.msg)
        else:
            pass
        cursor.close()
        self.connector.commit()
        return item

    def close_spider(self, spider):
        self.connector.commit()

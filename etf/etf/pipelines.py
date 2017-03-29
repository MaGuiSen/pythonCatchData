# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
import pandas as pd
import logging


class EtfPipeline(object):
    def __init__(self):
        # self.engine = create_engine('mysql+mysqlconnector://yiping:Yiping@123@117.29.166.222:1206/robo_chat',
        #                             echo=False)

        self.engine = create_engine('myssssssql+mysqlconnector://yiping:Yiping@123@117.29.166.222:1206/robo_chat',
                                    echo=False)

    def process_item(self, item, spider):
        fun_name = 'process_' + item['item_type']

        method = getattr(self, fun_name)
        if not method:
            raise NotImplementedError("Method %s not implemented" % fun_name)
        method(item, spider)

    def process_hk_etl_list(self, item, spider):
        df = pd.DataFrame(item['item_list'])
        df.to_sql('etf_hk_list', self.engine, if_exists='append', index=False, index_label=['id'])

    def process_us_etl_list(self, item, spider):
        df = pd.DataFrame(item['item_list'])
        df.to_sql('etf_us_list', self.engine, if_exists='append', chunksize=1000, index=False, index_label=['id'])

    def process_cn_etl_list(self, item, spider):
        df = pd.DataFrame(item['item_list'])
        df.to_sql('etf_cn_list', self.engine, if_exists='append', chunksize=1000, index=False, index_label=['id'])

    def process_douban_movie_item(self,item,spider):
        exits = self.engine.execute('select 1 from douban_movies where douban_id='+item['item_data']['douban_id'])
        if exits.rowcount:
            pass
        else :
            df = pd.DataFrame([item['item_data']])
            df.to_sql('douban_movies', self.engine, if_exists='append', chunksize=1000, index=False, index_label=['douban_id'])

    def process_douban_novel_item(self,item,spider):
        exits = self.engine.execute('select 1 from douban_novel where douban_id=' + item['item_data']['douban_id'])
        if exits.rowcount:
            pass
        else:
            df = pd.DataFrame([item['item_data']])
            df.to_sql('douban_novel', self.engine, if_exists='append', chunksize=1000, index=False,
                      index_label=['douban_id'])

    def process_hk_cna_news(self,item,spider):
        exits = self.engine.execute('select 1 from hk_cna_news where news_date=%s and title=%s',
            (item['item_data']['news_date'],item['item_data']['title']))
        if exits.rowcount:
            pass
        else:
            df = pd.DataFrame([item['item_data']])
            df.to_sql('hk_cna_news', self.engine, if_exists='append', chunksize=1000, index=False,
                      index_label=['id'])

    def process_baidu_music_hot500(self,item,spider):
        df = pd.DataFrame(item['item_list'])
        df.to_sql('baidu_music_hot500', self.engine, if_exists='append', chunksize=1000, index=False,
                  index_label=['id'])

# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

import utils.configutils as cu
from mysql.connector import MySQLConnection
import utils.validator as validator


class SaveToDBPipeline(object):
    def __init__(self):
        self.configPath = "./utils/config/db_config_inner.ini"
        self.dbconfig = cu.read_db_config(self.configPath)
        self.connector = MySQLConnection(charset='utf8', **self.dbconfig)

    def process_item(self, item, spider):
        fun_name = 'process_' + item['pipeline_type']
        method = getattr(self, fun_name)
        if not method:
            raise NotImplementedError("Method %s not implemented" % fun_name)
        method(item, spider)

    def process_IPItem(self, item, spider):
        if item:
            cursor = self.connector.cursor()
            sql_query = 'insert into ip_address (ip,port,address,ip_type) values (%s,%s,%s,%s)'
            cursor.execute(sql_query, (item['ip'], item['port'], item['address'], item['ip_type']))
            cursor.close()
            self.connector.commit()


class CheckProxyIpPipeline(object):
    """
        检测代理ip的可用性
    """

    def process_item(self, item, spider):
        if item['pipeline_type'] == 'IPItem':
            # 进行检测可用性，然后存放到数据库
            is_useful = validator.checkProxyIp_1(item['ip'], item['port'], 'http://wwww.baidu.com')
            if is_useful:
                return item
            raise DropItem

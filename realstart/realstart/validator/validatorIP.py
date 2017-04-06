# -*- coding: utf-8 -*-
import os

from ..utils import configutils as cu
from mysql.connector import MySQLConnection
from ..utils import validator


class validatorIP(object):
    def __init__(self):
        self.configPath = os.path.join(os.path.dirname(__file__) + '/../utils/config/db_config_inner.ini')
        self.dbconfig = cu.read_db_config(self.configPath)
        self.connector = MySQLConnection(charset='utf8', **self.dbconfig)
        pass

    def start(self):
        # 从数据库中取出所有IP，正常情况下IP不多
        cursor = self.connector.cursor()
        sql_query = 'select id,ip,port from ip_address'
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for id, ip, port in results:
            # 判断可用性
            is_useful = validator.checkProxyIp_1(ip, port, 'http://wwww.baidu.com')
            if not is_useful:
                # 不可用的需要將对应ip从数据库中剔除
                sql_del = 'delete from ip_address where ip=%s'
                cursor.execute(sql_del, (ip,))
                self.connector.commit()
            else:
                print 'useful'
        return True
# validatorService = validatorIP()
# validatorService.start()

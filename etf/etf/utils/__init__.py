#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import uuid
import pandas as pd


def query_params(url):
    """
    从url中提取查询参数
    :param url:
    :return: 查询参数字典
    """
    url_obj = urlparse.urlparse(url)
    params = urlparse.parse_qs(url_obj.query).items()
    return dict([(k, v[0]) for k, v in params])


def gen_request_uuid():
    """
    :return: 获取一个新的uuid
    """
    return uuid.uuid4().__str__()


def save_to_sql(engine, table_name, data_item):
    df = pd.DataFrame(data_item)
    df.to_sql('etf_us_list', engine, if_exists='append', chunksize=1000, index=False, index_label=['id'])

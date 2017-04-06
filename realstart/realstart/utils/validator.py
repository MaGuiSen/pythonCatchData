# -*- coding: utf-8 -*-
import requests
import telnetlib
import time


def checkProxyIp_1(ip='', port='', connect_url=''):
    """
    检测代理ip可用性 方法1
    :param ip:
    :param port:
    :param connect_url: 测试连接地址
    :return:
    """
    try:
        start_time = time.time()
        requests.get(connect_url, proxies={"http": "http://%s:%s" % (ip, port)}, timeout=5)
        back_time = time.time() - start_time
    except:
        return False
    else:
        return True


def checkProxyIp_2(ip, port):
    """
    检测代理ip可用性 方法2
    :param ip:
    :param port:
    :return:
    """
    try:
        start_time = time.time()
        telnetlib.Telnet(host=ip, port=port, timeout=10)
        back_time = time.time() - start_time
    except:
        return False
    else:
        return True


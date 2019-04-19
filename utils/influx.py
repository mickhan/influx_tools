#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'
import sys
from secret import ADMIN, PASSWD
from influxdb import InfluxDBClient


def conn(host, port, db):
    """
    连接influxdb
    :param host:
    :param port:
    :param db:
    :return:
    """
    try:
        client = InfluxDBClient(host, port, ADMIN, PASSWD, db)  # 初始化
        return client
    except Exception as e:
        print('Connect Client Error', str(e.args[0]))
        raise e


def query(conn, sql):
    """
    执行查询
    :param conn:
    :param sql:
    :return:
    """
    try:
        result = conn.query(sql)
        return result
    except Exception as e:
        print('Excute Sql Error', str(e.args[0]))
        raise e

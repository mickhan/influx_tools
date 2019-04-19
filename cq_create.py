#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

from utils.influx import conn, query
from settings import host, port, db


# SELECT (sum("total")-sum("slowRequest")-sum("error"))/sum("total") as SLA, sum("slowRequest")/sum("total") as Slow, sum("error")/sum("total") as Error FROM "rp_1h"."access_web_1h" WHERE time >= now() - 7d GROUP BY host,time(1d)
# 合并数据
def handleData(host, port, db, table):
    client = conn(host, port, db)
    tables_query = 'show field keys on ' + db + ' from rp_1m.' + table + '_1m'
    tables_list = query(client, tables_query)
    sql = ""
    for k, v in tables_list.items():
        for table_name in v:
            measurement_name = table_name["fieldKey"]
            sql = sql + 'sum("' + measurement_name + '") as "' + \
                  measurement_name + '",'

    cq_10m = 'create continuous query "cq_' + table + '_10m" on "' + db + '" RESAMPLE EVERY 10m for 30m begin select ' + \
             sql[:-1] + ' into "rp_10m"."' + table + '_10m" from "rp_1m"."' + \
             table + '_1m" group by time(10m),* end'
    cq_1h = 'create continuous query "cq_' + table + '_1h" on "' + db + '" RESAMPLE EVERY 1h for 2h begin select ' + \
            sql[:-1] + ' into "rp_1h"."' + table + '_1h" from "rp_10m"."' + \
            table + '_10m" group by time(1h),* end'
    cq_6h = 'create continuous query "cq_' + table + '_6h" on "' + db + '" RESAMPLE EVERY 6h for 12h begin select ' + \
            sql[:-1] + ' into "rp_6h"."' + table + '_6h" from "rp_1h"."' + \
            table + '_1h" group by time(6h),* end'

    result_10m = query(client, cq_10m)
    result_1h = query(client, cq_1h)
    result_6h = query(client, cq_6h)
    print(result_10m, result_1h, result_6h)


def main():
    for tb in ["measurement_name"]:
        try:
            handleData(host, port, db, tb)
        except Exception as e:
            print(str(e))
            print(tb)


if __name__ == '__main__':
    main()

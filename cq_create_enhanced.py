#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

import re
from utils.influx import conn, query
from settings import host, port, db, rp, postfix, resample

# SELECT (sum("total")-sum("slowRequest")-sum("error"))/sum("total") as SLA, sum("slowRequest")/sum("total") as Slow, sum("error")/sum("total") as Error FROM "rp_1h"."access_web_1h" WHERE time >= now() - 7d GROUP BY host,time(1d)
# 合并数据

TPL_CREATE_CQ = "CREATE CONTINUOUS QUERY %s ON %s %s BEGIN SELECT %s INTO %s FROM %s GROUP BY time(%s),* END"
TPL_SHOW_FIELD = "SHOW FIELD KEYS ON %s FROM %s"
TPL_RESAMPLE = "RESAMPLE EVERY %s FOR %s"
DEFAULT_DURATION = rp[0]


def generate_measurement_fullname(db, measurement, duration, post_fix=True):
    rp = "autogen" if duration == "autogen" else "rp_" + duration
    if post_fix:
        fullname = "\"%s\".\"%s\".\"%s_%s\"" % (db, rp, measurement, duration)
    else:
        fullname = "\"%s\".\"%s\".\"%s\"" % (db, rp, measurement)
    return fullname


def generate_resample(target_duration):
    """
    >>> generate_resample("10m")
    'RESAMPLE EVERY 10m FOR 20m'
    >>> generate_resample("6h")
    'RESAMPLE EVERY 6h FOR 12h'
    """
    res = re.findall("^(\d+)([a-z]+)$", target_duration)
    time_length = int(res[0][0])
    time_granularity = res[0][1]
    return TPL_RESAMPLE % (target_duration, str(time_length*2)+time_granularity)


def get_fields(db, measurement, default_duration, post_fix=True):
    fullname = generate_measurement_fullname(db, measurement, default_duration, post_fix)
    tables_query = TPL_SHOW_FIELD % (db, fullname)
    client = conn(host, port, db)
    return query(client, tables_query)


def handle_data(host, port, db, measurement):
    client = conn(host, port, db)
    tables_list = get_fields(db, measurement, DEFAULT_DURATION, postfix)
    select_sentence = ""
    for _, v in tables_list.items():
        select_sentence = ", ".join(["sum(\""+item["fieldKey"]+"\") as \""+item["fieldKey"]+"\"" for item in v])

    for i in range(1, len(rp)):
        source_duration = rp[i-1]
        target_duration = rp[i]
        tables_query = TPL_CREATE_CQ % (
            "\"cq_"+measurement+"_"+target_duration+"\"",
            db,
            generate_resample(target_duration) if resample else "",
            select_sentence,
            generate_measurement_fullname(db, measurement, target_duration, postfix),
            generate_measurement_fullname(db, measurement, source_duration, postfix),
            target_duration
        )
        # print(tables_query)
        res = query(client, tables_query)
        print(res)


def main():
    for tb in ['measurement_name']:
        try:
            handle_data(host, port, db, tb)
        except Exception as e:
            print(str(e))
            print(tb)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

from utils.influx import conn, query
from settings import host, port, db


def main():
    q = r"SHOW CONTINUOUS QUERIES"

    c = conn(host, port, db)
    res = query(c, q)
    # print(res)
    for db_struct, res_list in res.items():
        db_name, _ = db_struct
        if db_name == db:
            for item in res_list:
                print(item["name"])
                # print(item["query"])


if __name__ == '__main__':
    main()

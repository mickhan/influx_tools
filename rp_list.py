#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

from utils.influx import conn, query
from settings import host, port, db


def main():
    q = r"SHOW RETENTION POLICIES ON %s"

    c = conn(host, port, db)
    res = query(c, q % db)
    # print(res)
    for db_struct, res_list in res.items():
        print(list(map(lambda x: x.split("_")[-1], [item["name"] for item in res_list])))


if __name__ == '__main__':
    main()

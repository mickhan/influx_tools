#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

from utils.influx import conn, query
from settings import host, port, db


def main():
    q = r"SHOW MEASUREMENTS ON %s"

    c = conn(host, port, db)
    res = query(c, q % db)
    for db_struct, res_list in res.items():
        print(list(set(map(lambda x: x.rsplit("_", 1)[0], [item["name"] for item in res_list]))))


if __name__ == '__main__':
    main()

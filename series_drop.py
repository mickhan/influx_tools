#!/usr/bin/env python
# -*- coding: utf-8 -*-

__mtime__ = '2018/12/17'

import sys
from utils.influx import conn, query
from settings import host, port, db


def main():
    start = sys.argv[1]
    with open("./resoulution.log") as f:
        for line in f.readlines():
            line = line.strip()
            if start and int(line) < int(start):
                continue
            print(line)
            q_drop = "drop series from chaos_monitor_data where resolution='%s'" % line
            c = conn(host, port, db)
            res = query(c, q_drop)
            print(res)


if __name__ == '__main__':
    main()

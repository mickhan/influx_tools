#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.influx import conn, query
from settings import host, port, db


def main():
    with open("./meas_to_del") as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            # q_drop = 'drop MEASUREMENT "%s"' % line
            c = conn(host, port, db)
            # print(q_drop)
            # res = query(c, q_drop)
            res = c.drop_measurement(line)
            print(res)
            # break

if __name__ == '__main__':
    main()

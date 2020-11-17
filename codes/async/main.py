#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/11/17 17:15
import time
from blocking import blocking_way
from nonblocking import non_blocking_way

cost_time = 0
try_count = 10


def time_it(foo_func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = foo_func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time - start_time
        func_name = foo_func.__name__
        if not res:
            return func_name, cost_time
        return res, func_name, cost_time

    return wrapper


@time_it
def sync_way(func):
    """
    阻塞执行10次，返回结果
    """
    res = [func() for _ in range(try_count)]
    return len(res)


def main():
    for func in [blocking_way, non_blocking_way]:
        ret = sync_way(func)
        print(func.__name__, ret)


if __name__ == '__main__':
    main()

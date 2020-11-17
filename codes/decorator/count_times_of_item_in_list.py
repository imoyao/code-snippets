#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 https://www.zhihu.com/question/27800240
 https://www.oschina.net/question/2400361_2151742
'''
import time
import collections

import numpy as np

# reload(sys)
# sys.setdefaultencoding("utf-8")


import settings


cost_time = 0


def time_it(func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time-start_time
        return res, cost_time
    return wrapper

# @time_it
# def read_excel():
#     fname = settings.EXCEL_PATH_FILE
#     workfile = xlrd.open_workbook(fname)  # type=list
#     sheet_name = workfile.sheet_names()[0].encode("utf-8")  # sheet name
#     table = workfile.sheet_by_index(0)
#     foo_list = table.col_values(1)
#     useful_data_list = foo_list[5:-1]
#     return useful_data_list


@time_it
def set_count(foo_list):
    # foo_list = ["a","b","c","a","b","a","b","c","a","b"]
    foo_dict = {}
    for item in set(foo_list):
        foo_dict[item] = foo_list.count(item)
    return foo_dict


@time_it
def list_count(foo_list):

    foo_dict = {}
    for item in foo_list:
        foo_dict[item] = foo_list.count(item)
    return foo_dict


@time_it
def counter(foo_list):
    rets = dict(collections.Counter(foo_list))

    return rets


def generate_data(num=1000000):
    return np.random.randint(num / 10, size=num)


@time_it
def unique(foo_list):
    return dict(zip(*np.unique(foo_list, return_counts=True)))

if __name__ == '__main__':
    num = int(raw_input("please enter an int bigger than 10:"))
    foo_list = list(generate_data(num))

    n = unique(foo_list)
    # print n
    n_t = n[1]

    a = set_count(foo_list)
    # print a
    set_t = a[1]

    c = counter(foo_list)
    count_t = c[1]

    # b = list_count(foo_list)
    # list_t = b[1]

    # print "set_count cost {}".format(timeit.timeit("set_count(generate_data(10000))",setup="from __main__ import set_count,generate_data",number = 1000))


    # print "counter cost {}".format(timeit.timeit("counter(generate_data(10000))",setup="from __main__ import counter,generate_data",number = 1000))

    # print "unique cost {}".format(timeit.timeit("unique(generate_data(10000))",setup="from __main__ import unique,generate_data",number = 1000)) 

    # print "list_count cost {}".format(timeit.timeit("list_count(generate_data(10000))",setup="from __main__ import list_count,generate_data",number = 1000))


    # print n
    # print a
    # print b
    # print c
    time_list = [set_t, count_t, n_t]
    print time_list
    time_list.sort()
    print time_list
    # num > 1000时:n,c,s,l
    # num = 100时:s,c,n,l
    # num = 250时:...
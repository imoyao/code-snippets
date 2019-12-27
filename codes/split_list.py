#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/27 11:35

import timeit
import math
import json


def split_list(alist, split_len):
    """
    按照每4个一组进行划分
    :param alist:
    :param split_len:
    :return:
    """
    b = []
    start_split_index = 0
    length = int(math.ceil(len(alist) / float(split_len)))
    while length > 0:
        a = []
        end_index = start_split_index + split_len
        for i in alist[start_split_index:end_index]:
            a.append(i)

        start_split_index += split_len

        length -= 1
        b.append(a)

    return b


def make_four_column(data):
    """
    返回 4 列数据
    :param data:
    :return:
    """
    a = []
    b = []
    c = []
    d = []
    print(data)
    for item in data:
        a.append(item[0])
        b.append(item[1])
        c.append(item[2])
        d.append(item[3])
    return [a[::-1], b[::-1], c[::-1], d[::-1]]


def list_of_groups(init_list, children_list_len):
    list_of_group = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def slice_it(li, cols=4):
    start = 0
    length = int(math.ceil(len(li) / float(cols)))
    for i in range(length):
        stop = start + len(li[i::cols])
        yield li[start:stop]
        start = stop


def slice_list(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def zip_iter(seq, size):
    return list(zip(*[iter(seq)] * size))


def make_iter(num):
    """
    模拟组装 disk 信息
    :param num:
    :return:
    """
    disk_list = []
    for i in range(num):
        disk = {'name': f'sd{i}',
                'num': i,
                'state': i % 2 == 0}
        disk_list.append(disk)
    return disk_list


def main(iter_len, column_num):
    """

    :param iter_len:
    :param column_num:
    :return:
    """
    alist = make_iter(iter_len)
    print(alist)
    d1 = split_list(alist, column_num)
    t1 = make_four_column(d1)
    data = {'info': t1}
    return json.dumps(data)


if __name__ == '__main__':
    # t1 = main()
    # a = 24
    # num = 4
    # # t2 = list_of_groups(a, num)
    # # d1 = split_list(a, num)
    # t1 = main(a, num)

    # t1 = timeit.timeit(stmt="split_list(a, num)",
    #                    setup="from __main__ import split_list, a,num", number=1000)
    # t2 = timeit.timeit(stmt="list_of_groups(a, num)",
    #                    setup="from __main__ import list_of_groups, a,num", number=1000)
    a = list(range(24))
    num = 4
    t1 = split_list(a, num)
    t2 = list_of_groups(a, num)
    t3 = slice_list(a, num)
    t4 = zip_iter(a, num)
    print(t1)
    print(t2)
    print(t3)
    print(t4)

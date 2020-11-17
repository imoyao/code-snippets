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


def make_four_column(data, column_num=4):
    """
    返回 column_num 列数据
    :param data:
    :param column_num:
    :return:
    """

    def append_item(seq, _item, index):
        try:
            item_in = _item[index]
            # if not item_in:
            #     item_in = {"name": "", "num": None, "state": False}

        except IndexError:
            # item_in = {"name": "", "num": None, "state": False}
            item_in = {}
        seq.append(item_in)

        return seq

    a = []
    b = []
    c = []
    d = []

    for item in data:
        for i in range(column_num):
            if i == 0:
                a = append_item(a, item, 0)
            elif i == 1:
                b = append_item(b, item, 1)
            elif i == 2:
                c = append_item(c, item, 2)
            elif i == 3:
                d = append_item(d, item, 3)
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
    # print(alist)
    alist = [{'name': 'sd0', 'num': 0, 'state': True}, {'name': 'sd1', 'num': 1, 'state': False},
             {},
             {},
             {},
             {'name': 'sd8', 'num': 8, 'state': True}, {'name': 'sd9', 'num': 9, 'state': False},
             {},
             {'name': 'sd12', 'num': 12, 'state': True}, {'name': 'sd13', 'num': 13, 'state': False},
             {'name': 'sd14', 'num': 14, 'state': True}, {'name': 'sd15', 'num': 15, 'state': False},
             {},
             {'name': 'sd18', 'num': 18, 'state': True}, {'name': 'sd19', 'num': 19, 'state': False},
             {'name': 'sd20', 'num': 20, 'state': True}, {'name': 'sd21', 'num': 21, 'state': False},
             {}]

    d1 = slice_list(alist, column_num)
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
    # a = list(range(2))
    # num = 4
    # t1 = split_list(a, num)
    # t2 = list_of_groups(a, num)
    # t3 = slice_list(a, num)
    print(main(24, 4), '--------')
    # t4 = zip_iter(a, num)
    # print(t1)
    # print(t2)
    # print(t3)
    # print(t4)

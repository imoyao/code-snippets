#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random
# 列表[0,0,0,1,1,2,3,3,3,2,3,3,0,0]分割成[[0, 0, 0], [1, 1], [2], [3, 3, 3],[2], [3, 3], [0, 0]]
# Q from: https://www.zhihu.com/question/49735791


def random_list(list_len):
    rand_list = []
    while len(rand_list) < list_len:
        i = random.randrange(0, 5)
        j = random.randrange(0, 3)
        rand_list.extend([i]*j)
    return rand_list[:list_len]


def start_item_index(alist):
    ret = None
    if not ret:
        ret = []
    for index, item in enumerate(alist):
        if alist[index-1] != alist[index]:
            ret.append(index)
    return ret


def group_by_item(alist, index_list):
    result = None
    if not result:
        result = []
    frist_res = alist[:index_list[0]]
    if frist_res:
        result.append(frist_res)
    # result.append(alist[:index_list[0]])
    # alist = [0, 0, 1, 2, 2, 0, 2, 2, 2, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 2]
    # alist = [2, 1, 1, 2, 1, 2, 0, 0, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 0, 0]
    for i, j in enumerate(index_list):
        if i < len(index_list) - 1:
            result.append(alist[j:index_list[i+1]])
    result.append(alist[index_list[-1]:])
    return result


def main(alist):
    # print("the given list is: {0}".format(alist))
    index_list = start_item_index(alist)
    group_list = group_by_item(alist, index_list)
    return group_list


if __name__ == '__main__':

    alist = random_list(20)
    time1s = time.time()
    print(main(alist))
    time1e = time.time()
    print("===========DRY============")
    time2s = time.time()
    from itertools import groupby
    print([list(v) for k, v in groupby(alist)])
    time2e = time.time()
    print ("time1 is {:.16f}".format(time1e-time1s))
    print ("time2 is {:.16f}".format(time2e-time2s))

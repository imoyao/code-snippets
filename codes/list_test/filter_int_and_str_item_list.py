#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
找出列表中大写开头的（去除空格后）和int型，并按照原来的索引顺序返回新列表
['Ha', 'World', 666, 8, 5, 'Python', u'Www']
'''

alist = ['Ha', '   hello', 'World   ', 666, 8, 'de', '12', 5, 'Python', u'Www']
copy_list = alist[:]


def int_list(alist):
    item_index = dict()
    ret = dict()
    for index, item in enumerate(alist):
        item_index.update({item: index})
    # print (item_index)
    # 找出列表中大写开头的（去除空格后）和int型，并返回新列表
    int_list = [int(numstr) for numstr in [
        intnum for intnum in alist if isinstance(intnum, int)]]  # int_str_list
    ret['item_index'] = item_index
    ret['int_list'] = int_list
    return ret
# print (int_list)
# print "#######int_list"


def filter_list(alist, int_item_dict):
    #[8, 5, 'World', 'Python']
    int_list = int_item_dict['int_list']
    for j in int_list:
        alist.remove(j)
    # print alist
    # [item for item in alist if item.strip().istitle()]  #newlist
    # int元素和istitle元素组成新的列表
    int_list.extend([item for item in alist if item.strip().istitle()])
    return int_list



def sort_index_list(int_str_list, int_item_dict):
    index_list = []
    item_index = int_item_dict['item_index']
    # print item_index
    for key in int_str_list:
        index_list.append(item_index[key])
    sort_indexlist = sorted(index_list)
    return sort_indexlist


def int_and_stripstr(sort_indexlist,copy_list):
    ret = []
    for i in sort_indexlist:
        if isinstance(copy_list[i], int):
            ret.append(copy_list[i])
        elif isinstance(copy_list[i], basestring):
            ret.append(copy_list[i].strip())
        else:
            pass
    return ret


def main(alist):
    int_lists = int_list(alist)
    int_str_list = filter_list(alist, int_lists)
    sort_indexlist = sort_index_list(int_str_list, int_lists)
    ret = int_and_stripstr(sort_indexlist,copy_list)
    return ret

if __name__ == '__main__':
    res = main(alist)
    print(res)
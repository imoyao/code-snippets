#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

current_path = os.path.join(os.getcwd(), os.path.dirname(__file__))


def get_dir_info(params=None):
    if not params:
        params = dict()
    rtndata = {}
    childnodes = []
    childnode = {}
    id_num = 'id' in params and params['id'] or '0'
    path = 'path' in params and params['path'] or current_path
    if os.path.exists(path) and os.path.isdir(path):
        items = os.listdir(path)
        nums = len(items)
        for index in range(0, nums):
            filename = items[index]
            fileid = '{0}_{1}'.format(id_num, str(index))
            file_path = os.path.join(path, items[index])
            if os.path.isdir(file_path):
                isdir = True
            else:
                isdir = False
            childnode['id'] = fileid
            childnode['name'] = filename
            childnode['path'] = file_path
            childnode['isdir'] = isdir
            childnodes.append(childnode)
            childnode = {}
    rtndata['state'] = '0'
    rtndata['result'] = childnodes
    return rtndata


if __name__ == '__main__':
    print(current_path)
    params = dict()
    path = 'F:/MYcode/somecode/'
    params['path'] = path
    res = get_dir_info(params)
    print type(res)
    data_json = json.dumps(res)
    print(data_json)
    print type(data_json)

    if not isinstance(res, str):
        retdatas = str(res)
    filenum = retdatas.count('False')
    dirnum = retdatas.count('True')

    print(filenum, dirnum)

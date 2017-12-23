#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import hashlib

'''
http://www.sharejs.com/codes/python/7142
https://www.cnblogs.com/ma6174/archive/2012/05/05/2484415.html
https://www.cnblogs.com/perfei/p/6138214.html
https://www.cnblogs.com/maseng/p/3386140.html       文件系统属性
'''

current_path = os.path.join(os.getcwd(), os.path.dirname(__file__))

cost_time = 0
'''
    print(current_path)
    params = dict()
    path = 'F:/MYcode/somecode/'
    params['path'] = path
    res = get_dir_info(params)
    retdatas = json.dumps(res)
    filenum = retdatas.count('false')
    dirnum = retdatas.count('true')

    print(filenum, dirnum)
'''


def get_dir_info(params=None):      # TODO:os.walk()
    if not params:
        params = dict()
    rtndata = {}
    childnodes = []
    id_num = 'id' in params and params['id'] or '0'
    file_type = 'type' in params and params['type'] or None
    filenum = 0
    path = 'path' in params and params['path'] or current_path
    if os.path.exists(path) and os.path.isdir(path):
        for fp, dirs, fs in os.walk(path):
            for f in fs:
                childnode = {}
                if file_type:       # 文件类型过滤
                    # os.path.splitext(i)[1]
                    if f.split('.')[-1] == file_type:
                        f = f
                    else:
                        continue
                else:
                    pass
                filenum += 1
                childnode['id'] = '{0}_{1}'.format(id_num, str(filenum))
                childnode['name'] = f
                childnode['path'] = os.path.join(fp, f)
                childnodes.append(childnode)
    # print childnodes
    rtndata['state'] = '0'
    rtndata['result'] = childnodes
    return rtndata


def get_md5(filename):
    with open(filename,'rb') as f:
        md5_val = hashlib.md5()
        while True:
            data = f.read(2048)
            if not data:
                break
            md5_val.update(data)
        return md5_val.hexdigest()


def get_file_size(fp):
    if os.path.exists(fp) and os.path.isfile(fp):
        f_size = os.path.getsize(fp)
    return f_size


def get_file_date(fp):
    """
    get file create date info
    :param fp: str file path
    :return: timestamp
    """
    if os.path.exists(fp) and os.path.isfile(fp):
        f_time = os.path.getctime(fp)
        return timestamp2strftime(f_time)


def timestamp2strftime(timestamp):
    """
    Convert timestamp to format time

    :param timestamp:float time like 1512377986.9297245
    :return:format str time like 2017-12-04 16:59:46
    """
    if not isinstance(timestamp, float):
        timestamp = float(timestamp)
    local_t = time.localtime(timestamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_t)
    return str_time


def time_it(foo_func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = foo_func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time-start_time
        func_name = foo_func.__name__
        if not res:
            return func_name, cost_time
        return res, func_name, cost_time
    return wrapper


@time_it
def main():
    if len(sys.argv) > 1:
        fp = sys.argv[1]
    else:
        fp = current_path
    params = dict()
    params['path'] = fp
    retinfos = get_dir_info(params)
    sizefinfos = dict()
    md5fpinfos = dict()
    deldatas = dict()
    delinfos = list()
    total_count = 0
    del_count = 0
    if retinfos and retinfos['state'] == '0':
        pathinfos = retinfos['result']
    if pathinfos:
        # print '===1111==={0}'.format(pathinfos)
        for item in pathinfos:
            total_count += 1
            filepath = item['path']
            filename = item['name']
            filesize = get_file_size(filepath)
            name_and_md5 = {'name': filename, 'md5': ''}
            # sizefinfos[filesize] = filepath
            # print '======{0}'.format(sizefinfos)
            if filesize in sizefinfos.keys():       # 若文件size相同则比对其md5
                # 若文件相同，则大小必然相等，但大小相等，不一定为同一文件
                filemd5 = get_md5(filepath)
                if not sizefinfos[filesize]['md5']:
                    sizefinfos[filesize]['md5'] = filemd5
                if filemd5 in sizefinfos[filesize]['md5']:
                    del_count += 1
                    delinfos.append(filepath)
                    deldatas[filemd5] = delinfos
                else:
                    deldatas[filemd5] = [filepath]
                    sizefinfos[filesize]['md5'] = filemd5
            else:
                sizefinfos[filesize] = name_and_md5

        return deldatas, total_count, del_count


@time_it
def mymain():
    if len(sys.argv) > 1:
        fp = sys.argv[1]
    else:
        fp = current_path
    params = dict()
    params['path'] = fp
    retinfos = get_dir_info(params)
    fileinfos = dict()
    filedict = dict()
    delfile = dict()
    ilkmd5s = list()
    md5li = []
    total_count = 0
    del_count = 0
    if retinfos and retinfos['state'] == '0':
        allfileinfos = retinfos['result']
    if allfileinfos:
        for item in allfileinfos:
            total_count += 1
            fp = item['path']
            filemd5 = get_md5(fp)
            createdate = get_file_date(fp)
            size = get_file_size(fp)
            filedatas = dict()
            filedatas['path'] = fp
            filedatas['id'] = item['id']
            filedatas['create'] = createdate
            filedatas['size'] = size
            if filemd5 not in fileinfos:
                fileinfos[filemd5] = [filedatas]
                # pass
            else:
                fileinfos[filemd5].append(filedatas)
            continue
        delitem = []
        ret = json.dumps(fileinfos)
        print('######1111111#####{0}'.format(ret))
        for k, val in fileinfos.items():
            md5_count = len(val)
            if md5_count > 1:
                del_count += 1
                delitem.append(val)

            '''
            if filemd5 not in md5li:
                md5li.append(filemd5)
            else:
                continue
            '''
    delinfos = json.dumps(delitem)       # 需删除条目
    # print('########111####{0},len:{1}'.format(res, count))
    return delinfos, total_count, del_count


def size_filter():
    if len(sys.argv) > 1:
        fp = sys.argv[1]
    else:
        fp = current_path
    params = dict()
    params['path'] = fp
    retinfos = get_dir_info(params)
    fileinfos = dict()
    total_count = 0
    del_count = 0
    if retinfos and retinfos['state'] == '0':
        allfileinfos = retinfos['result']
    if allfileinfos:
        for item in allfileinfos:
            total_count += 1
            fp = item['path']
            size = get_file_size(fp)
            filedatas = dict()
            filedatas['path'] = fp
            # filedatas['id'] = item['id']
            if size not in fileinfos:
                fileinfos[size] = [filedatas]
                # pass
            else:
                fileinfos[size].append(filedatas)
            continue
        ilksizedatas = [item['path'] for i in fileinfos.items() if len(i[1]) > 1 for item in i[1]]  # 过滤size唯一值file
        # size_ret = json.dumps(fileinfos)
    return ilksizedatas, total_count


if __name__ == '__main__':
    sizeinfos = size_filter()
    print(sizeinfos)
    print "*" * 20
    ret = main()
    print(ret)
    print "*"*20
    res = mymain()
    print(res)



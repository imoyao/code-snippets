#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import sys
import time
import json
import hashlib
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

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


def get_fp():
    """
    获取用户输入文件夹名称，缺省为当前程序所在文件夹
    :return: a str with dirname
    """
    if len(sys.argv) > 1:
        fp = sys.argv[1]
    else:
        fp = current_path
    return fp


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
                # childnode['name'] = f.decode('utf-8')
                childnode['name'] = f
                # childnode['path'] = os.path.join(fp, f).decode('utf-8')
                childnode['path'] = os.path.join(fp, f)
                # print(childnode['path'])
                childnodes.append(childnode)
    # print childnodes
    rtndata['state'] = '0'
    # print(childnodes)
    rtndata['result'] = childnodes
    return rtndata


def get_file_date(fp):
    """
    get file create date
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


def get_file_size(fp):
    if os.path.exists(fp) and os.path.isfile(fp):
        f_size = os.path.getsize(fp)
    return f_size


def get_md5(filename):
    with open(filename,'rb') as f:
        md5_val = hashlib.md5()
        while True:
            data = f.read(2048)
            if not data:
                break
            md5_val.update(data)
        return md5_val.hexdigest()


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
    fp = get_fp()
    params = dict()
    params['path'] = fp
    retinfos = get_dir_info(params)
    sizefinfos = dict()
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
            if filesize in sizefinfos.keys():       # 若文件size相同则比对其md5
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
        # print('######1111111#####{0}'.format(deldatas))
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
        # print('######1111111#####{0}'.format(ret))
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
    # print('########111####{0},len:{1}'.format(delinfos, del_count))
    return delinfos, total_count, del_count


def size_filter(allfileinfos):
    """
    根据文件大小分组
    :param allfileinfos: file info lists
    :return: file path list
    """
    total_count = 0
    fileinfos = dict()
    if allfileinfos:
        for item in allfileinfos:
            total_count += 1
            fp = item['path']
            size = get_file_size(fp)
            filedatas = dict()
            filedatas['path'] = fp
            if size not in fileinfos:
                fileinfos[size] = [filedatas]
                # pass
            else:
                fileinfos[size].append(filedatas)
            continue
        ilksizedatas = [item['path'] for i in fileinfos.items() if len(i[1]) > 1 for item in i[1]]  # 过滤掉size唯一值file
        # size_ret = json.dumps(fileinfos)
        return ilksizedatas, total_count


def md5_filter(dirid=None, aftersizedatas=None):
    """
    :param dirid: 文件夹编号 现为文件编号，唯一值，作为删除文件标识使用 TODO:对比多个文件夹时可作为参数
    :param aftersizedatas: 文件路径列表 list
    :return: MD5过滤之后的文件信息 json
    """
    fileinfos = dict()
    id_num = dirid if dirid else '0'
    filenum = 0
    if aftersizedatas:
        for fpitem in aftersizedatas:
            filemd5 = get_md5(fpitem)
            createdate = get_file_date(fpitem)
            size = get_file_size(fpitem)
            filedatas = dict()
            filedatas['path'] = fpitem
            filenum += 1
            filedatas['id'] = '{0}_{1}'.format(id_num, str(filenum))
            filedatas['create'] = createdate
            filedatas['size'] = size
            if filemd5 not in fileinfos:
                fileinfos[filemd5] = [filedatas]
            else:
                fileinfos[filemd5].append(filedatas)
            continue
        return fileinfos


def get_all_files():
    fp = get_fp()
    params = dict()
    params['path'] = fp
    retinfos = get_dir_info(params)     # 获取文件夹下文件信息
    # print(retinfos)
    # if retinfos and retinfos['state'] == '0':
    #     allfileinfos = retinfos['result']
    # else:
    #     rtndata['state'] = '1'
    #     result['message'] = 'get dirinfo failed'
    #     rtndata['result'] = result
    return retinfos


# @time_it
def getdouble():
    rtndata = dict()
    result = dict()
    after_md5_datas = dict()
    delinfos = list()
    total_count = 0
    retinfos = get_all_files()
    if retinfos and retinfos['state'] == '0':
        allfileinfos = retinfos['result']
    else:
        rtndata['state'] = '1'
        result['message'] = 'get dirinfo failed'
        rtndata['result'] = result
    # 获取文件夹信息结束
    # 判重开始
    # 若文件相同，则size必然相等，但大小相等，不一定为同一文件
    if allfileinfos:
        size_ret = size_filter(allfileinfos)
    else:
        rtndata['state'] = '1'
        result['message'] = 'get dirinfo failed'
        rtndata['result'] = result
    if size_ret:
        ilksizedatas = size_ret[0]
        total_count = size_ret[1]
    else:
        rtndata['state'] = '1'
        result['message'] = 'no same files by size'
        rtndata['result'] = result
        # return rtndata
    # 按照MD5分组
    if ilksizedatas:
        after_md5_datas = md5_filter(aftersizedatas=ilksizedatas)
    else:
        rtndata['state'] = '1'
        result['message'] = 'no same files by md5'
        rtndata['result'] = result
        # return rtndata
    # MD5过滤结束
    # print(after_md5_datas)
    if after_md5_datas:
        del_count = 0
        delitems = list()
        # ret = json.dumps(after_md5_datas)
        # print('######1111111#####{0}'.format(ret))
        for k, val in after_md5_datas.items():      # 判重，MD5值出现次数大于1，则为重复文件
            md5_count = len(val)
            if md5_count > 1:
                del_count += 1
                delitems.append(val)
        # delinfos = json.dumps(delitem)          # 需删除条目
        rtndata['state'] = '0'
        result['message'] = ''
        result['delinfos'] = delitems
        result['total_count'] = total_count
        result['del_count'] = del_count
        rtndata['result'] = result
        # return rtndata
    else:
        rtndata['state'] = '1'
        result['message'] = 'not same files after all'
        rtndata['result'] = result
    return rtndata


def showdouble():
    retdatas = getdouble()
    if retdatas and retdatas['state'] == '0':
        total_count = retdatas['result']['total_count'] or None
        del_count = retdatas['result']['del_count'] or None
        del_files = retdatas['result']['delinfos'] or None
    else:
        res = retdatas['result']['message']
        print(res)
        sys.exit(1)
    return total_count, del_count, del_files

'''
# 文件名是中文时，显示问题；
整体按大小排序，内部按时间排序 OrderedDict；    
see:
https://www.zhihu.com/question/50391422
http://blog.csdn.net/xiaminli/article/details/73381600
根据用户输入id进行文件删除,缺省删除

from findtools.find_files import (find_files, Match)

path='/Users/apple/node/test'
found_files = find_files(path)

for found_file in found_files:
print found_file
newname=found_file.replace('str1','')
os.rename(os.path.join(path,found_file),os.path.join(path,newname))
'''

if __name__ == '__main__':
    # sizeinfos = main()
    # print(sizeinfos[0][1:], sizeinfos[2])
    # print "*" * 20

    total_count, del_count, del_files = showdouble()

    print('''total files counts:{0};            # 总文件数
double files groups:{1};'''.format(total_count, del_count))     # 重复组
    if del_files:
        print('Those are duplicate files we found:')
        for item in del_files:
            item.sort(key=lambda x: x['create'])        # 对itemfile按照创建时间排序
            for fileinfo in item:
                print('id:{id}, size:{size}, create:{create}, path:{path}'.format(id=fileinfo['id'],
                                                                               size=fileinfo['size'],
                                                                               create=fileinfo['create'],
                                                                               path=fileinfo['path']))
            print("-" * 20)
    else:
        res = retdatas['result']['message']
        print(res)

    # print "*"*20
    #
    # res = mymain()
    # print(res[0][1:], res[2])



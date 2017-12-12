#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time


def walk_dir(dir_path,file_type_list):
    filelist = []
    for parent, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            if file and file.split(".")[-1] in file_type_list:
                filelist.append(os.path.join(parent,file))
    return filelist


def count_file_line(file_name):
    count = 0
    try:
        with open(file_name, 'r') as f:
            for line in f:
                if line:                        # with '\n'
                # if line and line != '\n':     # NOT '\n'
                    count += 1
        print ("{0: >10} ########## {1}".format(count, file_name))
        return count
    except Exception as e:
        raise e


def main():
    start_time = time.time()
    fname_or_dirpath = raw_input('please enter directory or file name you want count(default PWD):')  # TODO  if input file name and path
    currdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
    total = 0
    retcode = 0
    messg = ''
    result = {}
    if not fname_or_dirpath:
        fname_or_dirpath = currdir

    if fname_or_dirpath:
        if os.path.isfile(fname_or_dirpath):
            single_file_line = count_file_line(fname_or_dirpath)
            total += single_file_line

        elif os.path.isdir(fname_or_dirpath):
            file_type = raw_input('please enter Extension Name split with ",":')
            if file_type:
                file_type_list = file_type.split(',')
                filelist = walk_dir(fname_or_dirpath,file_type_list)
                for filename in filelist:
                    single_file_line = count_file_line(filename)
                    total += single_file_line
            else:
                retcode = 1
                total = None
                messg = "sorry,you should type a file type or path at least!"

    else:
        retcode = 2
        total = None
        messg = "sorry,please check your input for fname_or_dirpath?"

    cost_time = time.time() - start_time
    result = {"retcode": retcode, "total": total, "ctime": cost_time, "messg": messg}
    return result


if __name__ == '__main__':
    ret = main()
    if not ret['retcode']:
        print ("total:{0: >10}".format(ret['total']))
        print ("cost_time:{0: >5}".format(ret['ctime']))
    else:
        print ("The err messg is :{0: >10}".format(ret['messg']))
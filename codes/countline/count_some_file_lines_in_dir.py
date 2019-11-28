#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
file_type = raw_input('please enter Extension Name split with ",":')
file_type_list = file_type.split(',')
dir_path = raw_input('please enter directory name you want count:')
currdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
filelist = []

if not dir_path:
    dir_path = currdir

def get_file(dir_path):
    global file_type_list
    for parent, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            if file and file.split(".")[-1] in file_type_list:
                filelist.append(os.path.join(parent,file))
    return filelist

def count_file_line(file_name):
    count = 0
    with open(file_name, 'r') as f:
        for line in f:
            if line:                        # 计空行
            # if line and line != '\n':     # 不计空行
                count += 1
    print ("{0: >10} ########## {1}".format(count,file_name))
    return count

def main():
    start_time = time.time()
    total = 0
    filelist = get_file(dir_path)
    for filename in filelist:
        single_file_line = count_file_line(filename)
        total += single_file_line
    cost_time = time.time()-start_time
    print ("total:{0: >10}".format(total))
    print ("cost_time:{0: >5}".format(cost_time))
    return total

if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/12/20 10:37
"""
see also: 对os.walk中的topdown参数的理解 章节
"""
import os

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, 'root')
top_down_args = [True, False]
for top_down in top_down_args:
    print(f'Top_down is {top_down} ……')
    for root, dirs, files in os.walk(ROOT_PATH, topdown=top_down):
        if dirs:
            print(dirs, '=======ddd=========')
            dirs[:] = [dirs[0]]
            print(f'==after=slice====ddd====={dirs}====')
            for dir_item in dirs:
                print(f'dir is:{dir_item}')

        for f_item in files:
            print(f'file is {f_item}')
'''
Top_down is True ……
dir is:d0
dir is:d1
file is f0
dir is:d0_d1
file is d0_f0
file is d0_f1
file is d0_d1_f0
file is d1_f0

Top_down is False ……

file is d0_d1_f0
dir is:d0_d1
file is d0_f0
file is d0_f1
file is d1_f0
dir is:d0
dir is:d1
file is f0
'''

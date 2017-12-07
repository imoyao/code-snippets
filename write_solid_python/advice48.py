#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.cnblogs.com/fnng/p/3670789.html

import time
import threading


def play_music(*mu_names):
    for index, music in enumerate(mu_names):
        print('For {0},I am playing music:{1} at {2}.'.format(index, music, time.time()))
        time.sleep(1)


def watch_movie(*mv_names):
    for index, movie in enumerate(mv_names):
        print('For {0},I am watching movies:{1} at {2}.'.format(index, movie, time.time()))
        time.sleep(3)


def dos_time(mus_names, mvi_names):
    print('time for entertaining...', time.time())
    play_music(mus_names)
    watch_movie(mvi_names)
    print('time for sleeping...', time.time())
#####################


def couple_cpu_time(*args):
    thread_list = []
    print(args)
    mus_th = threading.Thread(target=play_music, args=args[0])
    thread_list.append(mus_th)
    mov_th = threading.Thread(target=watch_movie, args=args[1])
    thread_list.append(mov_th)
    print('time for entertaining...', time.time())
    for task in thread_list:
        task.setDaemon(True)        # 设置为守护进程
        task.start()
    time.sleep(3)
    print('time for sleeping...', time.time())


if __name__ == '__main__':
    mus_name_list = ['你', '精忠报国', '辣妹子']
    mvi_names_list = ['卧虎藏龙', '再见阿郎', '杀生']
    # dos_time(mus_name_list, mvi_names_list)
    print('======learn threading======')
    tasks = (mus_name_list, mvi_names_list)
    couple_cpu_time(*tasks)

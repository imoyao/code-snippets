#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.cnblogs.com/fnng/p/3670789.html
import time
import threading

cost_time = 0


def play_music(mu_names):
    for index, music in enumerate(mu_names):
        print('For {0},I am playing music:{1} at {2}.'.format(index, music, time.time()))
        time.sleep(1)


def do_homework(hwk_names):
    for index, homework in enumerate(hwk_names):
        print('For {0},I am doing homework:{1} at {2}.'.format(index, homework, time.time()))
        time.sleep(3)


def time_it(foo_func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = foo_func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time-start_time
        if not res:
            return cost_time
        return res, cost_time
    return wrapper


@time_it
def dos_time(mus_names, mvi_names):
    print('time for homeworking...', time.time())
    play_music(mus_names)
    do_homework(mvi_names)
    print('time for sleeping...', time.time())

#####################


@time_it
def couple_cpu_time(*args):
    thread_lists = []
    mus_th = threading.Thread(target=play_music, args=(args[0],))
    thread_lists.append(mus_th)
    hwk_th = threading.Thread(target=do_homework, args=(args[1],))
    thread_lists.append(hwk_th)
    print('time for entertaining...', time.time())
    for task in thread_lists:
        task.setDaemon(True)        # 设置为守护进程
        task.start()
    # time.sleep(2)
    task.join()
    print('time for sleeping...', time.time())


if __name__ == '__main__':

    mus_name_lists = ['山丘', '麦克', '历历万乡']
    homework_lists = ['数学', '语文', 'English']
    cost_time1 = dos_time(mus_name_lists, homework_lists)
    print('Do things one by one cost:{0}'.format(cost_time1))

    print('====== use threading ======')

    tasks = (mus_name_lists, homework_lists)
    cost_time2 = couple_cpu_time(*tasks)
    print('Do things together cost:{0}'.format(cost_time2))

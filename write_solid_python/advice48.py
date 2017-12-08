#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.cnblogs.com/fnng/p/3670789.html
import time
import threading

cost_time = 0


def play_music(mu_names):
    for index, music in enumerate(mu_names):
        print('For {0},I am playing music:{1} at {2}.'.format(
            index, music, time.time()))
        time.sleep(1)


def do_job(job_names):
    for index, job in enumerate(job_names):
        print('For {0},I am doing job:{1} at {2}.'.format(
            index, job, time.time()))
        time.sleep(3)


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
def noob_time(job_names, music_names):
    print('time for working...', time.time())
    do_job(job_names)
    play_music(music_names)
    print('time for Go-live...', time.time())

#####################


@time_it
def intermediate_time(music_names, job_names):
    thread_lists = []
    mus_th = threading.Thread(target=play_music, args=(music_names,))
    thread_lists.append(mus_th)
    job = threading.Thread(target=do_job, args=(job_names,))
    thread_lists.append(job)
    print('time for entertaining...', time.time())
    for task in thread_lists:
        task.setDaemon(True)        # 设置为守护进程
        task.start()
    # time.sleep(2)
    task.join()
    print('time for Go-live...', time.time())


if __name__ == '__main__':

    music_lists = ['山丘', '同桌的你', '历历万乡']
    job_lists = ['Program', 'Edit_Document', 'Debug']
    foo_name, noob_time = noob_time(job_lists, music_lists)
    print('Do things one by one({0}) cost:{1}'.format(foo_name, noob_time))

    print('====== use threading ======')
    time.sleep(1)

    bar_name, inter_time = intermediate_time(music_lists, job_lists)
    print('Do things together({0}) cost:{1}'.format(bar_name, inter_time))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@create: 2022/3/18 17:28
@file: join.py
@author: imoyao
@email: immoyao@gmail.com
@desc: 线程一直等待全部的子线程结束之后，主线程自身才结束，程序退出
"""
# import threading
# import time
#
#
# def run():
#     time.sleep(2)
#     print('当前线程的名字是： ', threading.current_thread().name)
#
#
# if __name__ == '__main__':
#
#     start_time = time.time()
#
#     print('这是主线程：', threading.current_thread().name)
#     thread_list = []
#     for i in range(5):
#         t = threading.Thread(target=run)
#         thread_list.append(t)
#
#     for t in thread_list:
#         t.setDaemon(True)
#         t.start()
#
#     for tj in thread_list:
#         tj.join()
#
#     print('主线程结束了！', threading.current_thread().name)
#     print('一共用时：', time.time() - start_time)
import threading
import time

cost_time = 0


def time_it(func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time - start_time
        return res, cost_time

    return wrapper


def princ(tring):
    print('task', tring)
    time.sleep(1)


@time_it
def main1():
    tlists = list()
    for i in range(5):
        t = threading.Thread(target=princ, args=('t-%s' % (i),))
        tlists.append(t)
        t.start()
        # 相当于单线程
        t.join()


@time_it
def main3():
    for i in range(5):
        princ(f't-{i}')


@time_it
def main2():
    tlists = list()
    for i in range(5):
        t = threading.Thread(target=princ, args=('t-%s' % (i),))
        tlists.append(t)
        t.start()
    # 注意两种join的区别
    for t in tlists:
        t.join()


if __name__ == '__main__':
    _, a = main1()
    _, b = main2()
    _, c = main3()
    print(a, b, c)

    # 当前线程执行完毕之后在执行后面的线程
    # t.join()

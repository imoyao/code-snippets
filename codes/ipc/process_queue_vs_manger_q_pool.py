#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@create: 2022/3/18 17:45
@file: pool_queue.py
@author: imoyao
@email: immoyao@gmail.com
@desc:
使用multiprocessing.Queue可以在进程间通信,但不能在Pool池创建的进程间进行通信
"""
import time
from multiprocessing import Manager, Pool, Queue, Process


def producer(queue):
    queue.put('A')
    time.sleep(2)
    print('put data')


def consumer(queue):
    time.sleep(2)
    data = queue.get()
    print("consumer:%s" % data)


def normal_q_with_process():
    queue = Queue(10)
    p = Process(target=producer, args=(queue,))
    c = Process(target=consumer, args=(queue,))
    p.start()
    c.start()
    p.join()
    c.join()


def manger_q_with_pool():
    # queue = Queue(10)  # type: ignore # 这个是使用multiprocessing.Queue,无效
    queue = Manager().Queue(10)  # 这个是使用multiprocessing.Manager.Queue, 可以
    pool = Pool(2)
    pool.apply_async(producer, args=(queue,))
    pool.apply_async(consumer, args=(queue,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    normal_q_with_process()
    manger_q_with_pool()

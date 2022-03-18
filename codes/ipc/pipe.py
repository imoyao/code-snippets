#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@create: 2022/3/18 17:56
@file: pip.py
@author: imoyao
@email: immoyao@gmail.com
@desc:
"""
import time
from multiprocessing import Process, Pipe


# 4.通过Pipe进行线程间的通信, pipe进程间通信的性能高于Queue
def producer(pipe):
    pipe.send('admin')


def consumer(pipe):
    data = pipe.recv()
    print("consumer:%s" % data)


if __name__ == '__main__':
    receive_pipe, send_pipe = Pipe()
    """Pipe只能适应于两个进程间的通信"""
    p = Process(target=producer, args=(send_pipe,))
    c = Process(target=consumer, args=(receive_pipe,))
    p.start()
    c.start()
    p.join()
    c.join()

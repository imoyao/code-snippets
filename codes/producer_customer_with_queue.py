#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao on 2018/5/9 14:05
"""
通过队列（Queue）实现生产者-消费者模型
"""

import threading
import time

# python2中
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class Producer(threading.Thread):
    def run(self):
        global count
        while True:
            if q.qsize() < 500:
                for i in range(300):
                    count += 1
                    good = 'good {}'.format(count)
                    q.put(good)
                    print('TOTAL:{},Producer {} create {}\n'.format(count, self.name, good))
                time.sleep(1)


class Customer(threading.Thread):
    def run(self):
        global count
        while True:
            if q.qsize() > 100:
                for i in range(100):
                    if not q.empty():
                        good = q.get()
                        count -= 1
                        print('TOTAL:{},Customer {} bug {}'.format(count, self.name, good))
                time.sleep(0.5)


def main():
    print('we have goods total {}'.format(q.qsize()))
    for _ in range(3):
        p = Producer()
        p.start()
    for _ in range(5):
        c = Customer()
        c.start()


if __name__ == '__main__':
    count = 500
    q = Queue()
    for i in range(500):
        q.put('stock {}'.format(i))
    main()

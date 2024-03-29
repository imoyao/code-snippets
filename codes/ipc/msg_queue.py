# -*- coding: utf-8 -*-
# @Time     : 2019/4/8 17:54
# @Author   : ELI
# @IDE      : PyCharm
# @PJ_NAME  : Queue


from multiprocessing import Process
from multiprocessing import Queue
from time import sleep


def write(q):
    for i in range(5):
        # sleep(1)
        print('put %s to queue..' % i)
        q.put(i)


def read(q):
    while 1:
        sleep(0.5)
        v = q.get(True)
        print('get %s from queue..' % v)


if __name__ == '__main__':
    q = Queue()  # type: ignore
    p1 = Process(target=write, args=(q,))
    p2 = Process(target=read, args=(q,))
    # p1.start()
    # p2.start()
    p1.join()  # 等待p1进程跑完后再往下执行
    # p2.join()
    #
    # while not q.empty():  # 队列不为空时阻塞在这
    #     sleep(1)
    #
    # p2.terminate()  # 结束p2进程
'''
put 0 to queue..
put 1 to queue..
put 2 to queue..
put 3 to queue..
put 4 to queue..
get 0 from queue..
get 1 from queue..
get 2 from queue..
get 3 from queue..
get 4 from queue..
'''
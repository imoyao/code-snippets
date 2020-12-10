#!/usr/bin/env python
# encoding: utf-8

import socket
import time
from concurrent import futures
from functools import wraps

REQ_DOMAIN = 'example.com'
cost_time = 0
try_count = 10


def time_it(foo_func):
    def wrapper(*args, **kwargs):
        global cost_time
        start_time = time.time()
        res = foo_func(*args, **kwargs)
        end_time = time.time()
        cost_time = end_time - start_time
        func_name = foo_func.__name__
        if not res:
            return func_name, cost_time
        return res, func_name, cost_time

    return wrapper


def blocking_way():
    """
    建立 socket 连接，发送HTTP请求，然后从 socket读取HTTP响应并返回数据。示例中我们请求 example.com 的首页。
    """
    sock = socket.socket()
    # 以blocking的方式向指定网址80端口发送网络连接请求
    sock.connect((REQ_DOMAIN, 80))
    request = f'GET / HTTP/1.0\r\nHost: {REQ_DOMAIN}\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    # 从socket上读取4K字节数据
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # blocking
        chunk = sock.recv(4096)
    return response


@time_it
def sync_way():
    """
    阻塞执行10次，返回结果
    """
    res = [blocking_way() for _ in range(try_count)]
    return len(res)


@time_it
def process_way():
    """
    进程池方式
    :return:
    """
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(try_count)}
    return len([fut.result() for fut in futs])


@time_it
def thread_way():
    """
    线程池方式
    """
    workers = 10
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(try_count)}
    return len([fut.result() for fut in futs])


def threadpool_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args, '#############')
        ret = []
        with futures.ThreadPoolExecutor(10) as executor:
            for item in args[0]:
                exc = executor.submit(func, item, **kwargs)
                ret.append(exc.result())
            # futures.wait(all_task, return_when=futures.ALL_COMPLETED)
        return ret

    return wrapper


def bar(item, is_test=True):  # TODO: 没有起到线程池的作用
    print(item, '-------123------')
    time.sleep(item)
    if is_test:
        num = 5
    else:
        num = 100
    return item + num


def threadpoolit(args, **kwargs):
    ret = []
    with futures.ThreadPoolExecutor(10) as executor:
        for item in args:
            exc = executor.submit(bar, item, **kwargs)
            ret.append(exc.result())
        # futures.wait(all_task, return_when=futures.ALL_COMPLETED)
    return ret


# @time_it
@threadpool_deco
def foo(item, is_test=True):  # TODO: 没有起到线程池的作用
    print(item, '-------------')
    time.sleep(item)
    if is_test:
        num = 5
    else:
        num = 100
    return item + num


def main():
    # a = sync_way()
    # print(a)
    # b = thread_way()
    # print(b)
    # c = process_way()
    # print(c)
    a = list(range(5))
    a1 = time.time()
    rettt = threadpoolit(a, is_test=True)
    aa1 = time.time()
    print(aa1 - a1, f'----{rettt}---------')

    t = time.time()

    d = foo(a, is_test=True)
    t1 = time.time()
    print(t1 - t, d)


if __name__ == '__main__':
    main()

"""
# count = 10
(10, 'sync_way', 0.3614327907562256)
(10, 'thread_way', 0.05895590782165527)
(10, 'process_way', 0.6955974102020264)
# count = 80
(80, 'sync_way', 5.538213014602661)
(80, 'thread_way', 1.2612965106964111)
(80, 'process_way', 1.0214107036590576)
"""

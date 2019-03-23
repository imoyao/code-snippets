#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 闭包、生成器、延迟绑定等

from functools import partial
from operator import mul


def multi_func():
    foo = []

    for i in range(5):
        def func(n):
            return n * i

        foo.append(func)

    return foo


def multi_func_starred():
    foo = []
    for i in range(5):
        def func(*n):
            return n * i

        foo.append(func)

    return foo


def multi_expression_starred():
    print(type(lambda *n: n * i for i in range(5)))
    return [lambda *n: n * i for i in range(5)]


def multi_expression():
    return [lambda n: n * i for i in range(5)]


def multi_expression_hack():
    return [lambda n, i=i: n * i for i in range(5)]


def gen_expression():
    return (lambda n: n * i for i in range(5))


def gen_func():
    for i in range(5):
        yield lambda n: i * n


def partial_func():
    return [partial(mul, i) for i in range(5)]


if __name__ == '__main__':
    print([func(10) for func in multi_expression_hack()])

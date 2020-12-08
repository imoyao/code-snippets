#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/9/3 20:59
import time
from functools import wraps


class Deco:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('out of real wrapper.')

        ret = self.func(*args, **kwargs)
        return ret


@Deco
def do_func():
    print('hello world')
    return 0


def do_bar():
    pass


if __name__ == '__main__':
    do_func()

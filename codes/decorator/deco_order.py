#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/9/3 22:05
import sys
import time
from functools import wraps


def check_has_set(func):
    """
    是否进行了模块配置
    :param func:
    :return:
    """
    print(f'out of func: {sys._getframe().f_code.co_name}')

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = None
        if 1 == 2:
            print(f'inner of func check_has_set.')
            ret = func(*args, **kwargs)
        return ret

    return wrapper


def check_has_enable(func):
    """
    模块是否启用
    :param func:
    :return:
    """
    print(f'out of func: {sys._getframe().f_code.co_name}')

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = None
        if 1 == 2:
            print(f'inner of func check_has_enable.')
            ret = func(*args, **kwargs)
        return ret

    return wrapper


def check_has_execute(func):
    """
    模块是否执行（是否可以抢占）
    :param func:
    :return:
    """
    time.sleep(5)
    print(f'out of wrapper,func: {sys._getframe().f_code.co_name}')

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = None
        if True:
            print(f'inner of func check_has_execute.')
            ret = func(*args, **kwargs)
        return ret

    return wrapper


@check_has_set
@check_has_enable
@check_has_execute
def foo():
    print('I can do it only when has_set and has_enable and before has_execute')


def bar():
    pass


if __name__ == '__main__':
    foo()
    # bar()
    # check_has_execute(check_has_enable(check_has_set(bar)))

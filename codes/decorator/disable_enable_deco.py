#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Administrator at 2020/9/5 10:49
from functools import wraps


def deco_it(func):
    """
    定义装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('----inner of wrapper before func----')
        ret = func(*args, **kwargs)
        print('----inner of wrapper after func--')
        return ret

    return wrapper


def another_deco_it(func):
    """
    定义另一个装饰器
    :param func:
    :return:
    """
    print('This is another deco.')

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret

    return wrapper


def disable_deco(func):
    """
    一个什么都没干的装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret

    return wrapper


GLOBAL_ENABLE_FLAG = True
depend_with_flag = deco_it if GLOBAL_ENABLE_FLAG else disable_deco


# @deco_it
# @another_deco_it
@depend_with_flag
def foo():
    print('Hello,World!')


if __name__ == '__main__':
    foo()
    # print('origin func under below.')
    # foo.__wrapped__()

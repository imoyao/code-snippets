#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/10 10:19
import timeit


def some_funky_data_structure(bar_data=None):
    class FunkyClass:

        def __init__(self):
            self.data = 'This is dunder init innner of FunkyClass'

        def get_funky(self, inner_data):
            print('The inner_data of inner get_funky() is {inner_data}, outer of inner data is {bar_data}.'.format(
                inner_data=inner_data, bar_data=bar_data))

    return FunkyClass


class _FunkyClass:

    def __init__(self, *args, **kwargs):
        print(f'args is {args},kwargs is {kwargs}.')
        self.data = 'This is dunder init innner of FunkyClass'
        self.bar_data = kwargs.get('bar_data', None)

    def get_funky(self, inner_data):
        print('The inner_data of inner get_funky() is {inner_data}, outer of inner data is {bar_data}.'.format(
            inner_data=inner_data, bar_data=self.bar_data))


def normal_some_funky_data_structure(bar_data=None):
    pass
    return _FunkyClass(bar_data=bar_data)


def call_normal_some_funky_data_structure():
    pass
    return _FunkyClass


class _Out:
    def test(self, _try_time=10):
        for i in range(_try_time):
            pass


def function_out(n, try_time):
    for _ in range(n):
        _Out().test(try_time)


def function_in(n, try_time):
    class Inner:
        def test(self, _try_time=10):
            for i in range(_try_time):
                pass

    for _ in range(n):
        Inner().test(try_time)


def function_mixed(n, try_time, cls=_Out):
    for _ in range(n):
        cls().test(try_time)


def func(num):
    num += 1
    return num


if __name__ == '__main__':
    foo = some_funky_data_structure('foo')
    foo_bar = some_funky_data_structure('foo_bar')
    print(foo().get_funky('baz'), foo_bar().get_funky('baz'))

    f1 = some_funky_data_structure()()
    f2 = some_funky_data_structure()()
    print(type(f1))
    print(type(f2))
    print(type(f1) is type(f2))
    print(isinstance(f1, type(f2)))
    f = _FunkyClass('a', 'b', bar_data='bar')
    f.get_funky('baz')

    # ===============

    foo = normal_some_funky_data_structure('foo')
    foo_bar = normal_some_funky_data_structure('foo_bar')
    foo.get_funky('baz')
    foo_bar.get_funky('baz')
    print(isinstance(foo, _FunkyClass))

    c_foo = call_normal_some_funky_data_structure()(bar_data='foo')
    c_fb = call_normal_some_funky_data_structure()(bar_data='foo_bar')
    c_foo.get_funky('baz')
    c_fb.get_funky('baz')
    print(isinstance(c_foo, _FunkyClass))

    # ===============

    m, test_try_time = 1, 10
    '''
    time of function_out is 0.0009663160890340805.
    time of function_in is 0.009836168959736824.    # 相差一个数量级
    time of function_mixed is 0.0009927581995725632.
    '''
    # m, test_try_time = 1000, 10
    '''
    time of function_out is 0.7052748203277588.
    time of function_in is 0.7609770204871893.
    time of function_mixed is 0.7371664671227336.
    '''
    # m, test_try_time = 10000, 10
    '''
    time of function_out is 6.49063076544553.
    time of function_in is 6.0502378745004535.
    time of function_mixed is 6.159397796727717.
    '''
    t1 = timeit.timeit(stmt="function_out(m, test_try_time)",
                       setup="from __main__ import function_out, m,test_try_time", number=1000)
    t2 = timeit.timeit(stmt="function_in(m, test_try_time)", setup="from __main__ import function_in, m,test_try_time",
                       number=1000)
    t3 = timeit.timeit(stmt="function_mixed(m, test_try_time)",
                       setup="from __main__ import function_mixed, m,test_try_time", number=1000)

    print(f'time of function_out is {t1}.')
    print(f'time of function_in is {t2}.')
    print(f'time of function_mixed is {t3}.')

    # ===============

    for i in map(lambda x: _FunkyClass.get_funky(x[1], x[0]),
                 [('foo', _FunkyClass(bar_data='foo_bar')), ('bar', _FunkyClass(bar_data='bar_foo'))]):
        pass

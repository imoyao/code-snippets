#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback


class People(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print('hello!')

    def programming(self):
        print('{0} can program with Python.'.format(self.name))


if __name__ == '__main__':
    pe = People('Peter', 23)
    # hasattr
    print(hasattr(pe, 'gender'))
    print(hasattr(pe, 'say_hello'))
    print('*'*20)

    # getattr
    print(getattr(pe, 'name'))
    try:
        getattr(pe, 'gender')
    except AttributeError as e:
        # traceback.print_exc()
        setattr(pe, 'gender', 'male')
    finally:
        print('After setattr,the gender is {0}'.format(getattr(pe, 'gender')))
    print('*'*20)

    # setattr
    if not hasattr(pe, 'score'):
        setattr(pe, 'score', 'A+')
    print(getattr(pe, 'score'))

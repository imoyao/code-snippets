#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/9 15:49
import random
import string

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))


if __name__ == '__main__':  # pragma:no cover
    cherrypy.quickstart(StringGenerator())

'''
pytest --cov test_code_12 --cov-report term-missing 12_pytest.py 
============================================================= test session starts ======================================
platform linux -- Python 3.7.3, pytest-5.3.1, py-1.8.0, pluggy-0.13.1
rootdir: /home/imoyao/mytemp/t_c_p
plugins: cov-2.8.1
collected 3 items                                                                                                                 

12_pytest.py ...                                                                                                                  

----------- coverage: platform linux, python 3.7.3-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
test_code_12.py       8      0   100%


============================================================== 3 passed in 0.69s =======================================

'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/9 15:51

import cherrypy
from cherrypy.test import helper

from test_code_12 import StringGenerator


class SimpleCPTest(helper.CPWebCase):

    @staticmethod
    def setup_server():
        cherrypy.tree.mount(StringGenerator(), '/', {})

    def test_index(self):
        self.getPage('/')
        self.assertStatus('200 OK')

    def test_generator(self):
        self.getPage('/generate')
        self.assertStatus('200 OK')

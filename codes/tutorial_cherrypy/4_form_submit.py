#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/7 16:35

import random
import string

import cherrypy


class StringGen:
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">                                   # get 请求
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, length=8):  # get 请求传参
        try:
            assert isinstance(length, int)
        except AssertionError:
            length = int(length)
        return ''.join(random.sample(string.hexdigits, length))


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})  # 开放外部访问
    cherrypy.quickstart(StringGen())

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/7 16:42
"""
https://docs.cherrypy.org/en/latest/tutorials.html#id8
"""
import random
import string

import cherrypy


class StringGen:
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">                            
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
        my_string = ''.join(random.sample(string.hexdigits, length))
        cherrypy.session['my_string'] = my_string
        return f"""
        Click here to get link:
        <a href="/display">{my_string}</a>
        """

    @cherrypy.expose
    def display(self):
        return cherrypy.session['my_string']  # 保存在内存中，重启app丢失


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})  # 开放外部访问
    cherrypy.quickstart(StringGen(), '/', conf)

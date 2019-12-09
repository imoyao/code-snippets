#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/9 10:17
"""
https://docs.cherrypy.org/en/latest/tutorials.html#id11
"""
import os
import random
import string

import cherrypy


class StringGen:

    @cherrypy.expose
    def index(self):
        return open('templates/index.html')


@cherrypy.expose
class StringGenWebServer:

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['my_string']

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['my_string'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['my_string'] = another_string

    def DELETE(self):
        cherrypy.session.pop('my_string', None)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './statics'
            }
        }
    }
    app = StringGen()
    app.generator = StringGenWebServer()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(app, '/', conf)

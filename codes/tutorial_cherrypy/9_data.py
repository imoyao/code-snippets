#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/9 11:05
"""
使用数据库
"""
import os
import random
import sqlite3
import string
import time

import cherrypy

DB_NAME = 'my.db'


class StringGen:

    @cherrypy.expose
    def index(self):
        return open('templates/index.html')

    @cherrypy.expose
    def ping(self):
        with sqlite3.connect(DB_NAME) as connector:
            # 由于sqlite禁止线程之间共享连接，而cherrypy是多线程服务器，所以每次调用都要使用with打开和关闭数据库连接，此处仅为演示，建议使用SQLAlchemy
            cherrypy.session['ts'] = time.time()
            r = connector.execute('SELECT value from user_string where session_id=?', [cherrypy.session.id])
            ret = r.fetchone()
            return ret


@cherrypy.expose
class StringGenWebServer:

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        with sqlite3.connect(DB_NAME) as connector:
            # 由于sqlite禁止线程之间共享连接，而cherrypy是多线程服务器，所以每次调用都要使用with打开和关闭数据库连接，此处仅为演示，建议使用SQLAlchemy
            cherrypy.session['ts'] = time.time()
            r = connector.execute('SELECT value from user_string where session_id=?', [cherrypy.session.id])
            ret = r.fetchone()
            return ret

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        with sqlite3.connect(DB_NAME) as connector:
            cherrypy.session['ts'] = time.time()
            connector.execute('INSERT Into user_string values (?,?)', [cherrypy.session.id, some_string])
        return some_string

    def PUT(self, another_string):
        with sqlite3.connect(DB_NAME) as connector:
            cherrypy.session['ts'] = time.time()
            connector.execute('update user_string SET value=? where session_id=?',
                              [another_string, cherrypy.session.id])

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_NAME) as connector:
            connector.execute('DELETE from user_string where session_id=?', [cherrypy.session.id])


def setup_db():
    """
    创建数据库
    :return:
    """
    with sqlite3.connect(DB_NAME) as con:
        con.execute('CREATE table user_string (session_id,value)')


def cleanup_db():
    """
    清空数据库
    :return:
    """
    with sqlite3.connect(DB_NAME) as con:
        con.execute('DROP TABLE if exists user_string')


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

        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './statics'
        }
    }
    # 创建和销毁数据库
    cherrypy.engine.subscribe('start', setup_db)
    cherrypy.engine.subscribe('stop', cleanup_db)

    app = StringGen()
    app.generator = StringGenWebServer()
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(app, '/', conf)

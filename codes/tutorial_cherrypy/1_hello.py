#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/7 15:29

import cherrypy


class HelloWorld:
    """
    see also:https://docs.cherrypy.org/en/latest/tutorials.html#id4
    """
    '''
    代码 @cherrypy.expose 则表明 index() 方法是要开放出去的.
    
    - 只有开放出去的方法,才可以处理各种HTTP请求.
    
    - 让开发人员自主控制对象的方法是否开放为Web请求更简单快捷.

    '''

    @cherrypy.expose
    def index(self):
        return 'Hello,World!'

    # index.exposed = True  # 与装饰器等效


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})  # 开放外部访问
    cherrypy.quickstart(HelloWorld())

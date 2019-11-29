#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 16:42
"""
在routing这一节中，我们可以按照 log 的严重等级做订阅；
但是，假如在系统中，我们需要先对不同的模块区分（auth,hardware,software），然后再去细分 log 等级（error,warning,info……），这个对不同模块的区分，就需要引入topic的概念

在<celerity>.<colour>.<species>这个实例中，我们可以假定为社交网站的话题，这个可以作为一个应用场景

- * 代表 1 个单词
- # 代表 0 个或多个单词
订阅者匹配到 topic，就可以收到该消息
不符合订阅规则的，将被**丢弃**（如：hello, er.duo.da.you.fu）
一个 # 的便是接受所有消息，类似exchange=fanout
当绑定中没有 * 和 # 时，表示 exchange 绑定是 direct 的
"""
import pika
import sys


def emitter():
    """
    发布者将消息给exchange，然后exchange分发给订阅者
    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
        severity = sys.argv[1] if len(sys.argv) > 2 else 'anonymons.info'
        msg = ' '.join(sys.argv[2:]) or 'Hello  World!'
        channel.basic_publish(exchange='topic_logs', routing_key=severity, body=msg)
        print(f'* Sending message {msg} from topic:{severity}.')


if __name__ == '__main__':
    emitter()

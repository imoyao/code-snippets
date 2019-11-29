#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 14:23
"""
https://www.rabbitmq.com/tutorials/tutorial-four-python.html
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
        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
        msg = ' '.join(sys.argv[2:]) or 'Hello  World!'
        channel.basic_publish(exchange='direct_logs', routing_key=severity, body=msg)
        print(f'* Sending message {severity}:{msg}')


if __name__ == '__main__':
    emitter()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 14:23

import pika
import sys


def emitter():
    """

    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        msg = ' '.join(sys.argv[1:]) or 'info: Hello  World!'
        channel.basic_publish(exchange='logs', routing_key='', body=msg)
        print(f'* Sending message {msg}')


if __name__ == '__main__':
    emitter()

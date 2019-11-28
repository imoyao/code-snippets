#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/21 15:55
"""
see also: https://www.jianshu.com/p/9c46a2ec2aa9
"""
import time
import pika


def product(channel, connection):
    channel.queue_declare(queue='test')
    channel.basic_publish(exchange='', routing_key='test', body='Hello World!')
    print('send "Hello world."')
    connection.close()


def main():
    print('[*] Sending messages. To exit press CTRL+C.')
    while True:
        pika_param = pika.ConnectionParameters(host='localhost')
        connection = pika.BlockingConnection(pika_param)
        channel = connection.channel()
        product(channel, connection)
        time.sleep(3)


if __name__ == '__main__':
    main()

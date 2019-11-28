#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/21 17:40
import pika


def callback(ch, method, properties, body):
    print(f"Received {body}")


def customer():
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='wzg')

    channel.basic_consume('test', callback, auto_ack=True)
    print('[*] Waiting for messages. To exit press CTRL+C.')
    channel.start_consuming()


if __name__ == '__main__':
    customer()

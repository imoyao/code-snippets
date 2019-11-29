#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/28 11:31
import pika
import sys


def sender():
    """
    round-robin 模式
    这种模式下，消息会被平等地投递给三个worker,后面加入更多worker 的话，也会接受后来的 task
    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        msg = ' '.join(sys.argv[1:]) or 'Hello  World!'
        channel.basic_publish(exchange='', routing_key='hello', body=msg)
        print(f'* Sending message {msg}')


def durable_sender():
    """
    与task.crush_ack_consumer()搭配使用，一个持久化的消息队列
    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='Bonjour', durable=True)    # 注意，两边都要声明自己是 durable 的
        msg = ' '.join(sys.argv[1:]) or 'Hello  World!'
        # channel.basic_publish(exchange='', routing_key='hello', body=msg)
        channel.basic_publish(exchange='',
                              routing_key='Bonjour',
                              body=msg,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent 持久化投递
                              ))
        print(f'* Sending message {msg}')


if __name__ == '__main__':
    # sender()
    durable_sender()

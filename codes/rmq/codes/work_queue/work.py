#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/28 11:20
"""
see also:https://www.rabbitmq.com/tutorials/tutorial-two-python.html
"""
import time
import pika


def consumer():
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_consume('hello', callback, auto_ack=True)
    print('[*] Waiting for messages. To exit press CTRL+C.')
    channel.start_consuming()


def callback(ch, method, prop, body):
    print(f'* Recving {body}.')
    wt = body.count(b'.')
    time.sleep(wt)
    print(f'* After wate for {wt} s, Done!')


def ack_consumer():
    """
    make auto_ack off
    一旦因为链路抖动导致消息没有被正常处理，则会触发重新投递机制
    :return:
    """
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    channel.basic_consume('hello', ack_callback)
    print('[*] Waiting for messages. To exit press CTRL+C.')
    channel.start_consuming()


def ack_callback(ch, method, prop, body):
    print(f'* Recving {body}.')
    wt = body.count(b'.')
    time.sleep(wt)
    print(f'* After waite for {wt} s, Done!')
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 此处不可缺少，否则虽然会执行任务，但是待处理任务队列不会被消耗，下次启动，还会继续执行
    # 内存会最终“爆炸”：`sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged` 查看


def crush_ack_consumer():
    """
    ack_consumer解决task重新投递问题，而 durable=True 解决rabbitMQ崩溃消息丢失问题
    :return:
    """
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='Bonjour', durable=True)

    channel.basic_consume('Bonjour', ack_callback)
    print('[*] Waiting for messages. To exit press CTRL+C.')
    channel.start_consuming()


def fair_dispatch_crush_ack_consumer():
    """
    ack_consumer解决task重新投递问题，而 durable=True 解决rabbitMQ崩溃消息丢失问题
    :return:
    """
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='Bonjour', durable=True)
    channel.basic_qos(prefetch_count=1)  # 公平处理，队列消息多于1条时，不再发给work,而是寻找空闲的消息队列
    channel.basic_consume('Bonjour', ack_callback)
    print('[*] Waiting for messages. To exit press CTRL+C.')
    channel.start_consuming()


if __name__ == '__main__':
    # consumer()        # 无应答确认消费
    # ack_consumer()  # 通过长短用时不一样的消息，我们可以看到，长时间的消息一旦被打断，此时会被还存在的worker接管该task
    # crush_ack_consumer()
    fair_dispatch_crush_ack_consumer()

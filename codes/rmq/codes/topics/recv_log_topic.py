#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 14:29
import sys
import functools
import pika

severities = sys.argv[1:]


def callback_func(ch, method, properties, body, topics):
    """
    关于callback函数传值问题：see also: https://github.com/pika/pika/issues/158

    :param ch:
    :param method:
    :param properties:
    :param body:
    :param topics:
    :return:
    """
    print(f"I am listening topic:{topics},Received from named topic:{method.routing_key} msg is:{body}")


def recviver(severities):
    """
    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs',
                                 exchange_type='topic')  # 注意，在发布订阅模式中我们使用fanout模式：此时下方routing_key会被ignore
        # queue=''生成随机临时queue，exclusice=True标识一旦适用房连接关闭，则立即删除队列
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        # severities = sys.argv[1:]
        if not severities:
            sys.stderr.write("Usage: %s [binging_topic_key]...\n" % sys.argv[0])
            sys.exit(1)
        for server in severities:
            channel.queue_bind(exchange='topic_logs', queue=queue_name,
                               routing_key=server)  # exchange 绑定 queue，也就是说只有它感兴趣“订阅”的频道，它才会“收听”到
        print(f'[*] Waiting for logs for topic:{severities}. To exit press CTRL+C.')
        # channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        # 此处使用偏函数，还有使用闭包的方案：https://github.com/pika/pika/issues/158
        channel.basic_consume(queue=queue_name, on_message_callback=functools.partial(callback_func, topics=severities),
                              auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    recviver(severities)

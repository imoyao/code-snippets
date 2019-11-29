#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 14:29
import pika
import sys


def callback(ch, method, properties, body):
    print(f"Received {method.routing_key} {body}")


def recviver():
    """
    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='direct_logs',
                                 exchange_type='direct')  # 注意，在发布订阅模式中我们使用fanout模式：此时下方routing_key会被ignore
        # queue=''生成随机临时queue，exclusice=True标识一旦适用房连接关闭，则立即删除队列
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        severities = sys.argv[1:]
        if not severities:
            sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
            sys.exit(1)
        for server in severities:
            channel.queue_bind(exchange='direct_logs', queue=queue_name,
                               routing_key=server)  # exchange 绑定 queue，也就是说只有它感兴趣“订阅”的频道，它才会“收听”到
        print('[*] Waiting for logs. To exit press CTRL+C.')
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    recviver()

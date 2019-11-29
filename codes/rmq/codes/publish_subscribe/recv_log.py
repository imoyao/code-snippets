#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/11/29 14:29
import pika


def callback(ch, method, properties, body):
    print(f"Received {body}")


def recviver():
    """

    :return:
    """
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        # queue=''生成随机临时queue，exclusice=True标识一旦适用房连接关闭，则立即删除队列
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='logs', queue=queue_name)  # 绑定
        print('[*] Waiting for messages. To exit press CTRL+C.')
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    recviver()

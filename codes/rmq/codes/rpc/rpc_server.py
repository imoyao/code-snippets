#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/12/16 15:07

import pika


def sender_consumer():
    pika_param = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(pika_param)
    channel = connection.channel()
    channel.queue_declare(queue='rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('rpc_queue', on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)
    print(f'request fib({n})')
    response = fib(n)
    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    sender_consumer()

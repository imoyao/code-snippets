# 用来学习`RabbitMQ`的使用
## 前置条件
```
(rmq) [imoyao@VM_0_16_centos rmq]$ sudo rabbitmqctl status | grep rabbit
Status of node rabbit@VM_0_16_centos
     [{rabbitmq_management,"RabbitMQ Management Console","3.6.10"},
      {rabbitmq_web_dispatch,"RabbitMQ Web Dispatcher","3.6.10"},
      {rabbitmq_management_agent,"RabbitMQ Management Agent","3.6.10"},
      {rabbit,"RabbitMQ","3.6.10"},
      {rabbit_common,
          "Modules shared by rabbitmq-server and rabbitmq-erlang-client",
          
(rmq) [imoyao@VM_0_16_centos rmq]$ python --version
Python 3.7.3

(rmq) [imoyao@VM_0_16_centos rmq]$ cat /etc/system-release
CentOS Linux release 7.6.1810 (Core) 
```
## 目录
- [Hello World](codes/hello_world/)
- [Work queues](codes/work_queue/)
- [Publish/Subscribe](codes/publish_subscribe/)
- [Routing](codes/routing/)
- [Topics](codes/topics/)
- [RPC](codes/rpc/)

## 参考
1. [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
2. [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)

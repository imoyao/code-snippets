#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import urllib2
import Queue


class SayHelloThread(threading.Thread):
    def run(self):
        print('{0} says hello at {1}'.format(self.name, time.time()))


def get_url_item(hosts):
    start_time = time.time()
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    for url in hosts:
        print('spider start to {0}'.format(url))
        request = urllib2.Request(url, headers=headers)
        page_detail = urllib2.urlopen(request)
        print(page_detail.read(1024))
    use_time = time.time()-start_time
    print('single use {0}'.format(use_time))


class DownloadThread(threading.Thread):

    def __init__(self, th_queue):
        threading.Thread.__init__(self)
        self.queue = th_queue

    def run(self):

        while True:
            url = self.queue.get()
            self.download_and_write_file(url)
            self.queue.task_done()
        print('write finished.\n')


    def download_and_write_file(self, url):
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        request = urllib2.Request(url, headers=headers)
        page_detail = urllib2.urlopen(request)
        tmp = page_detail.read(1024)
        if tmp:
            write_f(data)
        # with open('result.txt', 'wb') as f:
        #     tmp = page_detail.read(1024)
        #     if tmp:
        #         f.write(tmp)
        #         f.write('\n################\n')


def write_f(data):
    with open('result.txt', 'wb') as f:
        f.write(data)


def main(hosts):
    start_time = time.time()
    queue = Queue.Queue()
    for i in range(5):
        download_thr = DownloadThread(queue)
        download_thr.setDaemon(True)
        download_thr.start()

    for url_i in hosts:
        queue.put(url_i)

    queue.join()
    use_time = time.time() - start_time
    print('thread_queue use {0}'.format(use_time))


if __name__ == '__main__':
    # if：urllib2.URLError: <urlopen error [Errno 10054] >  try to change urls
    hosts = ['https://www.baidu.com', 'https://www.zhihu.com', 'https://www.sougou.com', 'https://www.so.com']
    main(hosts)
    # get_url_item(urls)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import urllib2
import Queue


# class SayHelloThread(threading.Thread):
#     def run(self):
#         print('{0} says hello at {1}'.format(self.name, time.time()))


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
            html = download_file(url)
            html_queue.put(html)
            # print('#########', html_queue.qsize())
            self.queue.task_done()
            # html_queue.task_done()

        print('write finished.\n')


def download_file(url):
    print('spider start to {0} at {1}'.format(url, time.time()))
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    request = urllib2.Request(url, headers=headers)
    page_detail = urllib2.urlopen(request)
    # tmp = page_detail.read(1024) + '\n################\n'
    tmps = page_detail.read(1024)
    # print(type(tmps))
    write_text = '\n'.join([line.strip() for line in tmps.split('\n') if line.strip()]) + '\n#####\n'   # 去除whitespace
    # print(write_text)
    return write_text


def get_html(hosts):
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


class WriteFileThread(threading.Thread):

    def __init__(self, txtFile):
        threading.Thread.__init__(self)
        # self.queue = th_queue
        self.wf_name = txtFile

    def run(self):
        mutex.acquire(1)
        with open(self.wf_name, 'a') as f:
            # print('###########', self.queue.qsize())
            # data = self.queue.get()
            data = html_queue.get()
            print('********', data)
            f.write(data)
        mutex.release()

        print('write finished.\n')


def write_file(txtFile):
    html_queue = Queue.Queue()

    for i in range(10):
        write_th = WriteFileThread(txtFile)
        write_th.setDaemon(True)
        write_th.start()

    html_queue.join()
    write_th.join()


if __name__ == '__main__':
    html_queue = Queue.Queue()
    # if：urllib2.URLError: <urlopen error [Errno 10054] >  try to change urls
    hosts = ['https://www.baidu.com', 'https://www.zhihu.com', 'https://www.sougou.com', 'https://www.so.com']
    get_html(hosts)
    txtFile = 'wftest.txt'
    mutex = threading.Lock()
    write_file(txtFile)


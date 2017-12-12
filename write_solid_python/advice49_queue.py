#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import Queue
import threading
import urllib2
# TODO


class DownloadThread(threading.Thread):
    def __init__(self, th_queue):
        threading.Thread.__init__(self)
        self.queue = th_queue

    def run(self):
        while True:
            url = self.queue.get()
            print('{name} is beginning with {url}:......\n'.format(name=self.name, url=url))
            self.download_file(url)
            self.queue.task_done()
            print('{name} download finished!\n'.format(name=self.name))

    def download_file(self, url):
        url_handler = urllib2.urlopen(url)
        fname = os.path.basename(url)+'.html'
        print('start write.\n')
        with open(fname, 'wb') as f:
            temp = url_handler.read(1024)
            # temp = url_handler.read()
            if temp:
                f.write(temp)
        print('write finished.\n')


if __name__ == '__main__':
    urls = ['https://www.baidu,com', 'https://www.qq.com', 'https://www.mi.com']
    queue = Queue.Queue()
    for i in range(5):
        download_thr = DownloadThread(queue)
        download_thr.setDaemon(True)
        download_thr.start()

    for url_i in urls:
        queue.put(url_i)

    queue.join()


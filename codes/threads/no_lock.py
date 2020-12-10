#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/12/10 16:06
import threading
import urllib.error
import urllib.request


class FetchUrls(threading.Thread):
    """
    Thread checking URLs.
    """

    def __init__(self, urls, output):
        """
        Constructor.

        @param urls list of urls to check
        @param output file to write urls output
        """
        super().__init__()
        self.urls = urls
        self.output = output

    def run(self):
        while self.urls:
            url = self.urls.pop()
            req = urllib.request.Request(url)
            d = None
            try:
                d = urllib.request.urlopen(req)
            except urllib.error.URLError as e:
                print(('URL %s failed: %s' % (url, e.reason)))
            if d:
                content = str(d.read(), encoding="utf8")
                self.output.write(content)
                print('write done by %s' % self.name)
                print('URL %s fetched by %s' % (url, self.name))


def main():
    # URL列表1
    urls1 = ['http://www.masantu.com', 'http://www.zhihu.com']
    # URL列表2
    urls2 = ['http://www.github.com', 'http://www.example.com']
    with open('output_no_lock.html', 'w', encoding='utf-8') as f:
        t1 = FetchUrls(urls1, f)
        t2 = FetchUrls(urls2, f)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == '__main__':
    main()

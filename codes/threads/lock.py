import threading
import urllib.error
import urllib.parse
import urllib.request


class FetchUrls(threading.Thread):
    """
    Thread checking URLs.
    """

    def __init__(self, urls, output, lock):
        """
        Constructor.

        @param urls list of urls to check
        @param output file to write urls output
        """
        super().__init__()
        self.urls = urls
        self.output = output
        self.lock = lock

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
                # 自动管理锁
                with self.lock:
                    print(f'lock acquired by {self.name}')
                    content = str(d.read(), encoding="utf8")
                    self.output.write(content)
                    print('write done by %s' % self.name)
                    print('URL %s fetched by %s' % (url, self.name))
                    print(f'lock release by {self.name}')


def main():
    # URL列表1
    urls1 = ['https://www.jisilu.cn/', 'http://www.zhihu.com']
    # URL列表2
    urls2 = ['http://www.github.com', 'http://www.example.com']
    lock = threading.Lock()
    with open('output_lock.html', 'w', encoding='utf-8') as f:
        t1 = FetchUrls(urls1, f, lock)
        t2 = FetchUrls(urls2, f, lock)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == '__main__':
    main()

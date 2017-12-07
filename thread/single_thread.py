# coding=utf-8
# codes from http://cenalulu.github.io/python/gil-in-python/
import time
from threading import Thread


def counter():
    i = 0
    for temp in range(10000000):
        i += 1
    return True


def main():
    thread_dict = {}
    start_time = time.time()
    for i in range(2):
        t = Thread(target=counter)
        t.start()
        t.join()
    take_time = time.time()-start_time
    print("It takes: {0}".format(take_time))


if __name__ == '__main__':
    main()

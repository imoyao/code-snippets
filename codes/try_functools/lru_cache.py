#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/12/14 11:22

import datetime
import random


class MyCache:

    def __init__(self):
        self.cache = dict()
        self.max_cache_size = 10

    def __contains__(self, item):
        return item in self.cache

    def get(self, item):
        data = self.cache.get(item)
        data['accessed'] = datetime.datetime.now()
        return data.get('value')

    def add(self, item_key, item_val):
        """
        添加元素，如果大于缓存最大值，则移除最旧元素
        :param item_key:
        :param item_val:
        :return:
        """
        if item_key not in self.cache and self.size >= self.max_cache_size:
            self.remove_oldest()
        self.cache[item_key] = {
            'accessed': datetime.datetime.now(),
            'value': item_val
        }

    def remove_oldest(self):
        """
        删除最旧元素
        :return:
        """
        oldest_item = None

        for item_key in self.cache:
            if oldest_item is None:
                oldest_item = item_key

            current_data_access = self.cache[item_key].get('accessed')
            oldest_data_access = self.cache[oldest_item].get('accessed')

            if current_data_access < oldest_data_access:
                oldest_item = item_key
        self.cache.pop(oldest_item)
    @property
    def size(self):
        return len(self.cache)


if __name__ == '__main__':
    cache = MyCache()
    cache.add('foo', sum(range(1000)))
    assert cache.get('foo') == cache.get('foo')
    print(cache.cache)
    key_list = [
        'red', 'fox', 'fence', 'junk', 'other', 'alpha', 'bravo', 'cal',
        'devo', 'ele'
    ]
    s = 'abcdefghijklmnop'
    for i, key_item in enumerate(key_list):
        if key_item not in cache:
            val = ''.join([random.choice(s) for i in range(20)])
            cache.add(key_item, val)

    # assert 'foo' not in cache
    print(cache.cache)
    print(cache.size)

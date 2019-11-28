# coding=utf-8
import heapq


class PriorityQueue(object):

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, power):
        heapq.heappush(self._queue, (-power, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)			# TODO

if __name__ == '__main__':
    q = PriorityQueue()
    q.push(Item('foo'), 1)
    q.push(Item('bar'), 3)
    q.push(Item('spam'), 5)
    q.push(Item('grok'), 1)
    print('*'*18)
    print q.pop()
    print q.pop()
    print q.pop()
    print q.pop()

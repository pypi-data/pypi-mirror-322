from collections import deque
from concurrent.futures import Future
from threading import Thread


class NonBlockingQueue:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.items = deque()
        self.getters = deque()
        self.putters = deque()

    def get_noblock(self):
        if self.items:
            if self.putters:
                self.putters.popleft().set_result(True)
            return self.items.popleft(), None
        else:
            fut = Future()
            self.getters.append(fut)
            return None, fut

    def put_noblock(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
            if self.getters:
                self.getters.popleft().set_result(self.items.popleft())
        else:
            fut = Future()
            self.putters.append(fut)
            return fut

    def get(self):
        item, fut = self.get_noblock()
        if fut:
            item = fut.result()
        return item

    def put(self, item):
        while True:
            fut = self.put_noblock(item)
            if fut is None:
                return
            fut.result()


def producer(q):
    for i in range(10):
        q.put(i)
        q.put(i * 10)
    q.put(None)


def consumer(q):
    while True:
        item = q.get()
        if item is None:
            return
        print(f"Got: {item}")


if __name__ == "__main__":
    q = NonBlockingQueue(2)

    Thread(target=producer, args=(q,)).start()
    Thread(target=consumer, args=(q,)).start()

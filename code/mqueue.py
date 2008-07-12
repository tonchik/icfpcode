from thread import *
from Queue import *
from threading import *

QueueMaxSize = 10000

class MQueue:
    def __init__(self, limit):
        self.queue = []
        self.lock  = RLock()
        self.nemptyevent = Event()
        self.nemptyevent.clear()
        if limit <= 0 :
            self.limit = QueueMaxSize
        else :
            self.limit = limit
    def put(self, obj):
        self.lock.acquire(True)
        if len(self.queue) == self.limit :
            print 'MQUEUE OVERFLOW, disgard message'
            self.queue.pop(0)
        self.queue.append(obj)
        self.nemptyevent.set()
        self.lock.release()

    def get(self):
        self.nemptyevent.wait()
        self.lock.acquire(True)
        obj = self.queue.pop(0)
        if len(self.queue) == 0:
            self.nemptyevent.clear()
        self.lock.release()
        return obj
    def isEmpty(self):
        self.lock.acquire(True)
        if len(self.queue) == 0:
            bEmpty = True
            self.nemptyevent.clear()
        else :
            self.nemptyevent.set()
            bEmpty = False
        self.lock.release()
        return bEmpty
    def isFull(self):
        self.lock.acquire(True)
        if len(self.queue) == self.limit:
            self.nemptyevent.set()
            bEmpty = True
        else:
            bEmpty = False
        self.lock.release()
        return bEmpty
    

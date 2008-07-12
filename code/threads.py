from thread import *
from Queue import *
from threading import *




QueueMaxSize = 10000

class MyQueue:
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
    
class Message:
    def __init__(self, data, bExit):
        self.data = data
        self.bExit = bExit
    def isExitMessage(self):
        return self.bExit
 
                
def threadFunc(msgQueue, ithread):
    while True:
        msg = msgQueue.get()
        if msg.isExitMessage() :
           break
        print 'thread num', ithread, msg.data
    print 'threadFunc exit'

def test():
    q1 = MyQueue(10000)
    q2 = MyQueue(10000)
    start_new_thread(threadFunc, tuple([q1, '1']))
    start_new_thread(threadFunc, tuple([q2, '2']))
    i = 0
    bExit = False
    while True:
        if i > 30000:
           bExit = True
        
        msg = Message(str(i), bExit)
            
        q1.put(msg)
        q2.put(msg)
        i = i+1
        if bExit:
            break
   
    print 'main thread exit'
   
if __name__ == '__main__':
    test() 


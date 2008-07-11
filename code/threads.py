from thread import *
from Queue import *
from threading import *

class Message:
    def __init__(self, data, bExit):
        self.data = data
        self.bExit = bExit
    def isExitMessage(self):
        return self.bExit
 
                
def threadFunc(msgQueue):
    while True:
        msg = msgQueue.get(True)
        if msg.isExitMessage() :
           break
        print msg.data
    print 'threadFunc exit'

def test():
    q1 = Queue(10000)
    q2 = Queue(10000)
    start_new_thread(threadFunc, tuple([q1]))
    start_new_thread(threadFunc, tuple([q2]))
    i = 0
    bExit = False
    while True:
        if i > 10000:
           bExit = True
        
        msg = Message(str(i), bExit)
            
        q1.put_nowait(msg)
        q2.put_nowait(msg)
        i = i+1
        if bExit:
            break
   
    print 'main thread exit'
   
if __name__ == '__main__':
    test() 


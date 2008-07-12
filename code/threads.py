from thread import *
from mqueue import *
from threading import *
import messages

class Message:
    def __init__(self, data, bExit):
        self.data = data
        self.bExit = bExit
    def isExitMessage(self):
        return self.bExit
 
                
def threadFunc(msgQueue, ithread):
    while True:
        msg = msgQueue.get()
        if msg[0] == messages.TERMINATE:
           break
        print 'thread num', ithread, msg[0]
    print 'threadFunc exit'

def test():
    q1 = MQueue(10000)
    q2 = MQueue(10000)
    start_new_thread(threadFunc, tuple([q1, '1']))
    start_new_thread(threadFunc, tuple([q2, '2']))
    i = 0
    bExit = False
    while True:
        if i > 30000:
       	    msg = (messages.TERMINATE,)
        else :
	    msg = (messages.TELE,)
        q1.put(msg)
        q2.put(msg)
        i = i+1
        if bExit:
            break
   
    print 'main thread exit'
   
if __name__ == '__main__':
    test() 


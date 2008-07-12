from threads import MyQueue
from threading import Thread

class Creator(Thread):
    def __init__(self, reader_to_creator):
        #print
        Thread.__init__(self)
        
    def run(self):
        print 'Creator started'
        try:
            pass
        except Exception, e:
            print e
        finally:
            pass


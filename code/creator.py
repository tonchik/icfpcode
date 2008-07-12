from threading import Thread
import messages

class Creator(Thread):
    def __init__(self, reader_2_creator):
        self.reader_2_creator = reader_2_creator
        Thread.__init__(self)
        
    def run(self):
        print 'Creator started'
        while True:
            msg = self.reader_2_creator.get()
            if msg[0] == messages.TERMINATE:
                break
        try:
            pass
        except Exception, e:
            print e
        finally:
            pass


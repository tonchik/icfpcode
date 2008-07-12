from threading import Thread

class Creator(Thread):
    def __init__(self, reader_to_creator):
        self.reader_to_creator = reader_to_creator
        Thread.__init__(self)
        
    def run(self):
        print 'Creator started'
        while True:
            msg = reader_to_creator.get()
            if msg[0] == messages.TERMINATE:
                break
        try:
            pass
        except Exception, e:
            print e
        finally:
            pass

